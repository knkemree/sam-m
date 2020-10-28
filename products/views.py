import http.client
import mimetypes
import json
import pandas as pd

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django import template
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage, Variation
from .forms import updateQtyForm

from cart.forms import CartAddProductForm
from cart.cart import Cart
from django.core.exceptions import ValidationError

register = template.Library()

@require_POST
def choose_size(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)
    print("product nedir")
    print(product)
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
            all_categories = []
            child_category = []
            parent_categories = Category.objects.filter(active=True, parent=None)
            parent_category = Category.objects.get(slug=category_slug, parent=None)
            parent_category_product_set = []
            child_categories = parent_category.children.all()
            
            if child_categories:
                for child_category in child_categories:
                    
                    child_category_product_set = Product.objects.filter(active=True, category=child_category)
                    for single_product in child_category_product_set:
                        parent_category_product_set.append(single_product)
            else:
                parent_category_product_set = Product.objects.filter(available=True, category=parent_category)
                child_category_product_set = []
            
        except:
            all_categories = Category.objects.filter(active=True)

            parent_category = []
            parent_categories = Category.objects.filter(active=True, parent=None)
            parent_category_product_set = []
            
            child_category = get_object_or_404(Category, slug=category_slug)
            child_categories = []
            child_category_product_set = Product.objects.filter(available=True, category=child_category )
 
    category = None
    
    categories = Category.objects.filter(active=True, parent=None)
    products = Product.objects.filter(available=True)
    
    cart_product_form = CartAddProductForm()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
        
        object_list = Product.objects.filter(available=True, category=category)
        paginator = Paginator(object_list, 20) # 3 posts in each page
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            products = paginator.page(paginator.num_pages)

    else:
        #shop sayfasini doldurabilmek icin asagidaki listlerin doldurulmasi veya ilgili listlerin olusturulmasi gerekiyor /products/ sayfasinda suan hicbirsey yok
        parent_category = []
        parent_categories = []
        parent_category_product_set = []
        child_category = []
        child_categories = []
        child_category_product_set = []
        all_categories = []
        object_list = Product.objects.filter(available=True)
        paginator = Paginator(object_list, 20) # 3 posts in each page
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            products = paginator.page(paginator.num_pages)


    return render(request,
                  'product_list_view.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'parent_category':parent_category,
                   'parent_categories':parent_categories,
                   'parent_category_product_set':parent_category_product_set,
                   'child_category':child_category,
                   'child_categories':child_categories,
                   'child_category_product_set':child_category_product_set,
                   'all_categories':all_categories,


                   'page': page,
                
                    'cart_product_form':cart_product_form,
                    
                    }
                    )



def product_detail_view(request, id, slug, variantid=None):
    
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    gallery = ProductImage.objects.filter(product_id=id)
    variant = None
    quantity_on_hand = 0
    #var = None
    #sizes = Variation.objects.filter(product_id=id, category="size")
    cart = Cart(request)
    
        
    if variantid:
        try:
            variant = Variation.objects.get(id=variantid)
            print(variant.ecomdashid)
            try:
                #eger ecomdashid'si sisteme dogru kayitli ve type:product ise
                
                conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
                payload = ''
                headers = {
                'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
                }
                conn.request("GET", "/api/Inventory?Type=Product&Id="+str(variant.ecomdashid), payload, headers)
                res = conn.getresponse()
                data = res.read()
                veri1 = json.loads(data.decode("utf-8"))
                sku = veri1["Sku"]

                
                conn.request("GET", "/api/Inventory?Type=Product&Sku="+str(sku), payload, headers)
                res = conn.getresponse()
                data = res.read()
                veri = json.loads(data.decode("utf-8"))
                #print(veri["data"])
                for i in veri["data"]:
                    quantity_on_hand = int(i["QuantityOnHand"])
                    
            except:
                #eger ecomdash id'si dogru degilse sisteme kayitli sku uzerinden quantity on hand'i bul
                try:
                    conn = http.client.HTTPSConnection("ecomdash.azure-api.net")
                    payload = ''
                    headers = {
                    'Ocp-Apim-Subscription-Key': 'ce0057d8843342c8b3bb5e8feb0664ac',
                    'ecd-subscription-key': '0e26a6d3e46145d5b7dd00a9f0e23c39'
                    }
                    conn.request("GET", "/api/Inventory?Type=Product&Sku="+str(variant.sku), payload, headers)
                    res = conn.getresponse()
                    data = res.read()
                    veri = json.loads(data.decode("utf-8"))
                    #print(veri["data"])
                    for i in veri["data"]:
                        quantity_on_hand = int(i["QuantityOnHand"])
                except:
                    pass

            #messages.success(request, "Size")
        except:
            pass
    

    #alttakini calistirinca sag ustte cartin icinde neler oldugunu gosteren acilir sekme product detail sayfasinda calismiyor. 
    #request.session["page"] = product.slug
    print(type(quantity_on_hand))
    return render(request,
                  'product_detail_view.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'gallery':gallery,
                  'variant':variant,
                  'quantity_on_hand':quantity_on_hand, 
                  'loop_times':range(1, int(quantity_on_hand)+1)
                  }
                  )

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
    clearance_products = Variation.objects.filter(clearance=True, active=True)
    cart_product_form = CartAddProductForm()
    context = {
        "clearance_products":clearance_products,
        'cart_product_form':cart_product_form,
        'loop_times':range(1, 15)
    }
    return render(request, "clearance.html", context)