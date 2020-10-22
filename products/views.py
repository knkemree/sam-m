from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Category, Product
from django.contrib.sessions.models import Session
from cart.forms import CartAddProductForm
from products.models import ProductImage, Variation

from django import template
from django.utils.safestring import mark_safe
from cart.cart import Cart

import http.client
import mimetypes
import json

register = template.Library()

@register.filter
def custom_filter(text, color):
    safe_text = '<span style="color:{color}">{text}</span>'.format(color=color, text=text)
    return mark_safe(safe_text)

# def show_category(request, hierarchy= None):
#     print("hierarchy")
#     print(hierarchy)
#     category_slug = hierarchy.split('/')
#     print("category_slug")
#     print(category_slug)
#     category_queryset = list(Category2.objects.filter(active=True))
#     all_slugs = [ x.slug for x in category_queryset ]
#     parent = None

#     for slug in category_slug:
#         if slug in all_slugs:
#             parent = get_object_or_404(Category2,slug=slug,parent=parent)
#             #parent = Category2.objects.filter(slug__in=category_slug, parent=None).first()
#         else:
#             instance = get_object_or_404(Product, slug=slug)
#             breadcrumbs_link = instance.get_cat_list()
#             category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
#             breadcrumbs = zip(breadcrumbs_link, category_name)
#             return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})

#     return render(request,"categories.html",{'post_set':parent.product_set.all(),'sub_categories':parent.children.all()})

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
                    print("selected variation id")
                    request.session["variation_id"] = variation.id
                    print(request.session.get("variation_id"))
                    messages.success(request, "Choosed size")
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
                    # try:
                    #     products_without_Child_category_but_has_parent_category = Product.objects.filter(active=True, category=parent_category)
                    #     parent_category_product_set = products_without_Child_category_but_has_parent_category
                    #     print("parentsiz urunler")
                    #     print(products_without_Child_category_but_has_parent_category)
                    # except:
                    #     pass
                    # parent_category_product_set2 = Product.objects.filter(active=True, category__parent=parent_category)
                    # print("oldu mu")
                    # print(parent_category_product_set2)
                    for single_product in child_category_product_set:
                        print("single burda mi")
                        print(single_product)
                        parent_category_product_set.append(single_product)
            else:
                parent_category_product_set = Product.objects.filter(available=True, category=parent_category)
                child_category_product_set = []
            
            print("asagida")
            print(parent_category_product_set)
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
    #gallery = ProductImage.objects.filter(product_id=id)

    # if parent_category_slug:
    #     parent_category = get_object_or_404(Category, slug=parent_category_slug, parent=parent)
    #     parent_category.children.all()

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
    quantity_on_hand = None
    #var = None
    #sizes = Variation.objects.filter(product_id=id, category="size")
    cart = Cart(request)
    
        
    if variantid:
        try:
            variant = Variation.objects.get(id=variantid)
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

            messages.success(request, "Size...")
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
                  'quantity_on_hand':quantity_on_hand} 
                  )
