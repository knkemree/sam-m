from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product
from django.contrib.sessions.models import Session
from cart.forms import CartAddProductForm
from products.models import ProductImage, Variation


def product_list_view(request, category_slug=None):
    
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    parent_cats = Category.objects.filter(parent__isnull=True)
    area_rugs = Category.objects.filter(parent_id=18)
    bed_sheets = Product.objects.filter(category_id=17)
    towels = Product.objects.filter(category_id=19)
    cart_product_form = CartAddProductForm()
    #gallery = ProductImage.objects.filter(product_id=id)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        #parent_cats_products =  products.filter(category__contains=category)
        print("product_list_view")
       # print(parent_cats_products)
        
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
                   'page': page,
                   'area_rugs': area_rugs,
                    'bed_sheets': bed_sheets,
                    'towels':towels,
                    'cart_product_form':cart_product_form,
                    
                    }
                    )



def product_detail_view(request, id, slug):
    
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    gallery = ProductImage.objects.filter(product_id=id)
    #sizes = Variation.objects.filter(product_id=id, category="size")
    print("product_detail_view")
    try:
        variant = Variation.objects.get(id=request.session.get("variation_id"))
        print(request.session.get("variation_id"))
    except:
        variant = {}
        print("variantin icindekiler")
        print(variant)
        pass
    #alttakini calistirinca sag ustte cartin icinde neler oldugunu gosteren acilir sekme product detail sayfasinda calismiyor. 
    #request.session["page"] = product.slug
    
    
    return render(request,
                  'product_detail_view.html',
                  {'product': product,
                  'cart_product_form': cart_product_form,
                  'gallery':gallery,
                  'variant':variant
                  #'sizes':sizes,
                  } 
                  )
