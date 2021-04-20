from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import FileForm
from .models import File
import pandas as pd
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from ship_station.forms import GTINForm
from ship_station.models import Brand, Color, InventoryLog, Model, Product, Size
import requests
import json
from gtin import GTIN
from django.views import generic

# Create your views here.

def model_form_upload(request):
    context ={}
    try:
        source = File.objects.latest('uploaded_at')
    except: 
        source = None
    print(source)
    
    if request.FILES.get('myfile', False):
        print('bu ya')
        

        form = FileForm()
        context['form'] = form

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)  
        

        file = pd.read_csv(source.document.path).dropna(subset=['SKU'])
        file['SKU'] = file['SKU'].astype(str)

        lookup = pd.read_csv(uploaded_file_url).dropna(subset=['SKU'])
        lookup['SKU'] = lookup['SKU'].astype(str)

        left_join = pd.merge(lookup, file, on ='SKU', how ='left')
        print(left_join)
        csv = left_join.to_csv(index=False)
        response = HttpResponse(csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename= "{}"'.format(myfile.name+".csv")
        return response
        
    elif request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
    else:
        form = FileForm()
    context['form'] = form
    context['source'] = source
    return render(request, 'qty_finder.html', context)

def update_source_file(request):
    form = FileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            form.save() 
    return render(request, 'update_source.html', {'form':form})
    
def lookup(request):
    context = {}
    try:
        source = File.objects.latest('uploaded_at')
    except: 
        source = None
    
    if request.FILES.get('myfile', False):
        print('bu ya')
        
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)  
        

        file = pd.read_csv(source.document.url).dropna(subset=['SKU'])
        file['SKU'] = file['SKU'].astype(str)

        lookup = pd.read_csv(uploaded_file_url).dropna(subset=['SKU'])
        lookup['SKU'] = lookup['SKU'].astype(str)

        left_join = pd.merge(lookup, file, on ='SKU', how ='left')
        print(left_join)
        csv = left_join.to_csv(index=False)
        response = HttpResponse(csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename= "{}"'.format(myfile.name)
        return response
    else:
        context['source']=source
        return render(request, 'v_lookup.html', context)

class IndexView(TemplateView):
    template_name = 'index.html'



def increase(request):
    data = {}
    form = GTINForm()
    if request.method == "POST" and request.is_ajax():
        form = GTINForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            gtin = form.cleaned_data.get('gtin')
            gtin = str(GTIN(raw='{}'.format(gtin)))
            try:
                product = Product.objects.get(gtin=gtin)
                log = InventoryLog.objects.create(product=product, quantity=1)
                
            except:
                headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                }
                resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(str(gtin)), headers=headers)
                data = json.loads(resp.text)
                for item in data['items']:
                    brand, created = Brand.objects.get_or_create(name=item['brand'])
                    model, created = Model.objects.get_or_create(brand=brand, name=item['model'])
                    color, created = Color.objects.get_or_create(name=item['color'])
                    size, created = Size.objects.get_or_create(name=item['size'])
                    product = Product.objects.create(name=item['title'],model=model,color=color,size=size,gtin=item['ean'])
                    log = InventoryLog.objects.create(product=product, quantity=1)
    
            data['gtin']=gtin
            return JsonResponse(data)
    return render(request, "increase.html", {"form": form})

def decrease(request):
    data = {}
    form = GTINForm()
    if request.method == "POST" and request.is_ajax():
        form = GTINForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            gtin = form.cleaned_data.get('gtin')
            gtin = str(GTIN(raw='{}'.format(gtin)))
            try:
                product = Product.objects.get(gtin=gtin)
                log = InventoryLog.objects.create(product=product, quantity=-1)
                
            except:
                headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                }
                resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(str(gtin)), headers=headers)
                data = json.loads(resp.text)
                for item in data['items']:
                    brand, created = Brand.objects.get_or_create(name=item['brand'])
                    model, created = Model.objects.get_or_create(brand=brand, name=item['model'])
                    color, created = Color.objects.get_or_create(name=item['color'])
                    size, created = Size.objects.get_or_create(name=item['size'])
                    product = Product.objects.create(name=item['title'],model=model,color=color,size=size,gtin=item['ean'])
                    log = InventoryLog.objects.create(product=product, quantity=-1)
    
            data['gtin']=gtin
            return JsonResponse(data)
    return render(request, "decrease.html", {"form": form})

class ProductDetailView(generic.DetailView):
    model = Product



