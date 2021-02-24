from .models import Product, Category

def menu(request):
    parent_categories = Category.objects.filter(active=True, parent=None).select_related('parent')
    child_categories1 = Category.objects.filter(active=True, parent__isnull=False).select_related('parent')

    try:
        area_rug = Category.objects.get(slug__contains="area-rugs")
        area_rugs = Category.objects.filter(parent_id=area_rug.id).select_related('parent')
    except:
        area_rugs = []
    
    try:
        bed_sheet = Category.objects.get(slug__contains="bed-sheets")
        bed_sheets = Product.objects.filter(category_id=bed_sheet.id).select_related('category')
    except:
        bed_sheets = []
    print("bed_sheets")
    print(bed_sheets)

    try:
        towel = Category.objects.filter(slug__contains="towels").select_related('parent')
        towels = Product.objects.filter(category_id=towel.id).select_related('category')
    except:
        towels= []

    return {'area_rugs': area_rugs,
            'bed_sheets': bed_sheets,
            'towels':towels,
            'parent_categories': parent_categories,
            'child_categories1':child_categories1,
            
            }