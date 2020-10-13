from .models import Product, Category

def menu(request):
    try:
        area_rug = Category.objects.get(slug__contains="area-rugs")
        area_rugs = Category.objects.filter(parent_id=area_rug.id)
    except:
        area_rugs = []
    
    try:
        bed_sheet = Category.objects.get(slug__contains="bed-sheets")
        bed_sheets = Product.objects.filter(category_id=bed_sheet.id)
    except:
        bed_sheets = []
    print("bed_sheets")
    print(bed_sheets)

    try:
        towel = Category.objects.filter(slug__contains="towels")
        towels = Product.objects.filter(category_id=towel.id)
    except:
        towels= []
        
    return {'area_rugs': area_rugs,
            'bed_sheets': bed_sheets,
            'towels':towels,
            }