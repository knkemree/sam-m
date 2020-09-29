from .models import Product, Category

def menu(request):
    area_rugs = Category.objects.filter(parent_id=18)
    bed_sheets = Product.objects.filter(category_id=17)
    towels = Product.objects.filter(category_id=19)
    return {'area_rugs': area_rugs,
            'bed_sheets': bed_sheets,
            'towels':towels,
            }