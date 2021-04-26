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
from re import search, IGNORECASE
from .forms import GTINForm
import time

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

class IndexView(FormView):
    template_name = 'index.html'
    form_class = GTINForm

    def form_valid(self, form):
        data = {}
        form.cleaned_data
        raw_number = str(form.cleaned_data.get('gtin'))
        print('string: ',raw_number)
        print('string length: ',len(str(raw_number)))
        if len(raw_number) >=14:
            for i in range(len(raw_number)-13):
                possible_gtin = raw_number[0+i:14+i]
                gtin = Product.objects.filter(gtin__icontains=possible_gtin)
                if len(gtin)>0:
                    print(gtin, 'gtin burda')
                    data['itemName'] = str(gtin[0])
                    data['itemQuantity'] = gtin[0].current_stock
                    return JsonResponse(data)
        else:
            data['itemName'] = 'Barcode invalid'
            data['itemQuantity'] = 'Not Found'
            return JsonResponse(data)

def convert_to_ean(number):
        return str(GTIN(raw='{}'.format(number)))

def increase(request):
    data = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    form = GTINForm()
    quantity = 1

    if request.method == "POST" and request.is_ajax():
        form = GTINForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            raw_number = str(form.cleaned_data.get('gtin'))
            print('string: ',raw_number)
            print('string length: ',len(str(raw_number)))
            if len(raw_number) >14:
                for i in range(len(raw_number)-13):
                    possible_gtin = raw_number[0+i:14+i]
                    gtin = Product.objects.filter(gtin__icontains=possible_gtin)
                    if len(gtin)>0:
                        print(gtin, 'gtin burda')
                        data['result'] = 'restocked'
                        InventoryLog.objects.create(product=gtin[0],quantity=quantity)
                        data['itemName'] = str(gtin[0])
                        data['itemQuantity'] = gtin[0].current_stock
                        return JsonResponse(data)
            elif len(raw_number) == 14:
                try:
                    product = Product.objects.get(gtin=raw_number)
                    InventoryLog.objects.create(product=product,quantity=quantity)
                    data['result'] = 'restocked'
                    data['itemName'] = str(product)
                    data['itemQuantity'] = product.current_stock
                except:
                    data['result'] = 'invalid_barcode'
                    data['itemName'] = 'This item does not exist. Check GTIN!'
                    data['itemQuantity'] = 'Not Found'
                return JsonResponse(data)
        else:
            data['result'] = 'invalid_barcode'
            data['itemName'] = 'This item does not exist. Check GTIN!'
            data['itemQuantity'] = 'Not Found'
            return JsonResponse(data)
            #print('form is not valid')
            #return render(request, "increase.html", {"form": form})
    else:
        print('no post or ajax request')
        return render(request, "increase.html", {"form": form})
            
    

def decrease(request):
    data = {}
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    quantity = -1
    form = GTINForm()
    if request.method == "POST" and request.is_ajax():
        form = GTINForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            raw_number = str(form.cleaned_data.get('gtin'))
            print('string: ',raw_number)
            print('string length: ',len(str(raw_number)))
            if len(raw_number) >=14:
                for i in range(len(raw_number)-13):
                    possible_gtin = raw_number[0+i:14+i]
                    gtin = Product.objects.filter(gtin__icontains=possible_gtin)
                    if len(gtin)>0:
                        print(gtin, 'gtin burda')
                        data['result'] = 'sold'
                        InventoryLog.objects.create(product=gtin[0],quantity=quantity)
                        data['itemName'] = str(gtin[0])
                        data['itemQuantity'] = gtin[0].current_stock
                        return JsonResponse(data)
            elif len(raw_number) == 14:
                try:
                    product = Product.objects.get(gtin=raw_number)
                    InventoryLog.objects.create(product=product,quantity=quantity)
                    data['result'] = 'sold'
                    data['itemName'] = str(product)
                    data['itemQuantity'] = product.current_stock
                except:
                    data['result'] = 'invalid_barcode'
                    data['itemName'] = 'This item does not exist. Check GTIN!'
                    data['itemQuantity'] = 'Not Found'
                return JsonResponse(data)
        else:
            data['result'] = 'invalid_barcode'
            data['itemName'] = 'This item does not exist. Check GTIN!'
            data['itemQuantity'] = 'Not Found'
            return JsonResponse(data)
    else:
        print('no post or ajax request')
        return render(request, "decrease.html", {"form": form})

class ProductDetailView(generic.DetailView):
    model = Product



class ProductListView(generic.ListView):
    model = Product
    paginate_by = 50

    def get_queryset(self):
        items =Product.objects.all()
        qs = [i.current_stock for i in items]
        return qs.sort(reverse=True)

class InventoryLogListView(generic.ListView):
    model = InventoryLog
    paginate_by = 50

    def get_queryset(self):
        logs = InventoryLog.objects.distinct('product_id').order_by('product_id')
        return logs