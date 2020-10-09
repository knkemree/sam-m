from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product
from django.contrib.sessions.models import Session
from cart.forms import CartAddProductForm
from products.models import ProductImage, Variation

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
                    
                    child_category_product_set = Product.objects.filter(available=True, category=child_category)
                    # try:
                    #     products_without_Child_category_but_has_parent_category = Product.objects.filter(available=True, category=parent_category)
                    #     parent_category_product_set = products_without_Child_category_but_has_parent_category
                    #     print("parentsiz urunler")
                    #     print(products_without_Child_category_but_has_parent_category)
                    # except:
                    #     pass
                    # parent_category_product_set2 = Product.objects.filter(available=True, category__parent=parent_category)
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
