import http.client
import mimetypes
import json
import pandas as pd
from itertools import chain

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django import template
from django.utils.safestring import mark_safe
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.core.exceptions import ValidationError

from .models import Category, Product, ProductImage, Variation
from .forms import updateQtyForm, SearchForm
from .tasks import get_stocks
from cart.forms import CartAddProductForm
from cart.cart import Cart


register = template.Library()

@require_POST
def choose_size(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        for item in request.POST:
            key = item
            val = request.POST[key]
            print("variant val and key")
            print(val, key)
            if val == "-----":
                try:
                    del request.session["variation_id"]
                except:
                    pass
            else:
                try:
                    variation = Variation.objects.get(product=product, category__iexact=key, title__iexact=val)
                    request.session["variation_id"] = variation.id  
                except:
                    pass

    # else:
    #     try:
    #         del request.session["variation_id"]
    #     except:
    #         pass

    
    return HttpResponseRedirect(url)
    #return redirect('products:product_detail_view_by_variant')
    
def product_list_view(request, category_slug=None):
    if category_slug:
        try:
            parent_category = Category.objects.get(slug=category_slug, parent=None)
        except:
            parent_category = None
        parent_categories = Category.objects.filter(active=True, parent=None).select_related('parent')

        if parent_category:
            #parent_category = Category.objects.get(slug=category_slug, parent=None)
            child_category = []
            # parent_category_product_set = []
            all_categories = []
        else:
            child_category = get_object_or_404(Category, slug=category_slug)
            all_categories = Category.objects.filter(active=True).select_related('parent')
            parent_category = []
            parent_category_product_set = []
    else:
        #shop sayfasini doldurabilmek icin asagidaki listlerin doldurulmasi veya ilgili listlerin olusturulmasi gerekiyor /products/ sayfasinda suan hicbirsey yok
        parent_category = []
        parent_categories = []
        child_category = []
        all_categories = []

    
    cart_product_form = CartAddProductForm()

    return render(request,
                  'product_list_view.html',
                  {'parent_category':parent_category,
                   'parent_categories':parent_categories,
                   'child_category':child_category,
                   'all_categories':all_categories,
                    'cart_product_form':cart_product_form,})



def product_detail_view(request, id, slug, variantid=None):
    
    product = get_object_or_404(Product, id=id)
    other_products = Product.objects.filter(available=True, category=product.category).exclude(id=id).select_related('category').select_related('category__parent')
    cart_product_form = CartAddProductForm()
    gallery = ProductImage.objects.filter(product_id=id).select_related('product')
    variant = None
    quantity_on_hand = 0
    cart = Cart(request)

    list_ids_or_sku = []

    try:
        for var in product.variation_set.all():
            api_id = var.sku
            list_ids_or_sku.append(api_id)

        payload1 = {"idType":"sku","idList":list_ids_or_sku}
        payload = str(payload1)
    except:
        for var in product.variation_set.all():
            api_id = var.ecomdashid
            list_ids_or_sku.append(api_id)

        payload1 = {"idType":"id","idList":list_ids_or_sku}
        payload = str(payload1)
    


    conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
    headers = {
    'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
    'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39',
    'Content-Type': 'application/json',
    'Authorization': 'Token 201105f43f33e2b5b287c55cd73823e0d050f537'
    }
    conn.request("POST", "/api/inventory/getProducts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    
    veri = json.loads(data.decode("utf-8"))
    veri2 = veri["data"]
     
    if variantid:
        try:
            variant = Variation.objects.get(id=variantid)
            for i in veri2:
                if int(float(i["Id"])) ==  int(float(variant.ecomdashid)):
                    quantity_on_hand = i["QuantityOnHand"]
        except:
            pass
    

    #alttakini calistirinca sag ustte cartin icinde neler oldugunu gosteren acilir sekme product detail sayfasinda calismiyor. 
    #request.session["page"] = product.slug
    
    return render(request,
                  'product_detail_view.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'gallery':gallery,
                  'variant':variant,
                  'quantity_on_hand':quantity_on_hand, 
                  'loop_times':range(1, int(quantity_on_hand)+1),
                  'other_products':other_products,
                  'veri2':veri2,})

def updateQtyView(request):

    if request.POST:
        form = updateQtyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                df_file = pd.read_csv(request.FILES["file"])
            except:
                df_file = pd.read_excel(request.FILES["file"])

      
      
            sku_list = df_file[df_file.columns[0]].tolist()
            new_stock_list = df_file[df_file.columns[1]].tolist()

            conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
            payload = ''
            headers = {
                'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
            }
            invalid_skus = []
            for sku, qty  in zip(sku_list, new_stock_list):
                
                try:
                    conn.request("GET", "/api/Inventory?Type=Product&Sku="+str(sku), payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    veri = json.loads(data.decode("utf-8"))
                    if len(veri["data"]) == 0:
                        invalid_skus.append(str(sku))
                    else:
                        for i in veri["data"]:
                            
                            updated_stock = int(i["QuantityOnHand"]) + int(qty) 

                        print("yeni stock")
                        print(updated_stock)

                        payload1 = [{'Sku': str(sku), 'Quantity': updated_stock, 'WarehouseId': 2019007911.0}]
                        payload = str(payload1)
                        headers = {
                            'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                            'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39',
                            'Content-Type': 'application/json'
                        }
                        conn.request("POST", "/api/inventory/updateQuantityOnHand", payload, headers)
                        res = conn.getresponse()
                        data = res.read()
                        print(data.decode("utf-8"))
                except:
                    pass
            
            if len(invalid_skus) == 0:
                messages.success(request,"Succesfully updated!")
            else:
                for i in invalid_skus:
                    messages.warning(request, "Invalid sku! Following sku couldn't update: "+str(i))
                    
        
            #csv = ecomdash_filterer(df_filter, filter_list)
            #csv = df_all_ecomdash[df_all_ecomdash["SKU Number"].isin(filter_list)].to_csv(index=False)
            #response = HttpResponse(csv, content_type='text/csv')
            #response['Content-Disposition'] = 'attachment; filename= "{}"'.format(request.FILES["upload"].name+".csv")
            #return response
            print(sku_list)
            print(new_stock_list)
    else:
        form = updateQtyForm()
    return render(request, "updateQty.html", {'form': form })

def clearance(request):
    clearance_products_list = Variation.objects.filter(sale_price__isnull=False, active=True).select_related('product__category').order_by('product__category','sku',)
    #clearance_products_exclude_zero = Variation.objects.filter(sale_price__isnull=False, active=True)
    # list_ids_or_sku = []
    # try:
    #     for variant in clearance_products:
    #         api_id = variant.sku
    #         list_ids_or_sku.append(api_id)   
    # except:
    #     for variant in clearance_products:
    #         api_id = variant.ecomdashid
    #         list_ids_or_sku.append(api_id)

    # result = get_stocks.delay(list_ids_or_sku)
    # try:
    #     try:
    #         clearance_products_exclude_zero = clearance_products.exclude(ecomdashid__in=result[0])
    #     except:
    #         clearance_products_exclude_zero = []
    # except:
    #     try:
    #         clearance_products_exclude_zero = clearance_products.exclude(sku__in=result[0])
    #     except:
    #         clearance_products_exclude_zero = []

    cart_product_form = CartAddProductForm(auto_id=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(clearance_products_list, 48) # 48 posts in each page
    clearance_products = paginator.page(1)

    try:
        clearance_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        clearance_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        clearance_products = paginator.page(paginator.num_pages)

    context = {
        "clearance_products":clearance_products,
        #'stocks':result[1],
        #'veri2':result[2],
        'cart_product_form':cart_product_form,
        'page':page,
        #'clearance_products_exclude_zero':clearance_products_exclude_zero
        #'loop_times':range(1, stock+1)
    }
    return render(request, "clearance.html", context)

def post_search(request):
    form = SearchForm()
    query = request.GET.get('query')
    results_list = []
    if query:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                results_list = Variation.objects.filter( Q(id__iexact=query)| Q(product__id__exact=query))
            except:
                results_list = Variation.objects.filter(Q(sku__icontains=query) )

    page = request.GET.get('page', 1)
    paginator = Paginator(results_list, 48) # 48 posts in each page
    results = paginator.page(1)

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        results = paginator.page(paginator.num_pages)       
            
    return render(request,
                  'search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'page':page,})