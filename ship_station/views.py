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
        raw_number = str(form.cleaned_data.get('gtin'))
        print('string: ',raw_number)
        print('string length: ',len(str(raw_number)))
        possible_eans = []
        if len(raw_number)>=12:
            for i in range(len(raw_number)-11):
                possible_upc = raw_number[0+i:12+i]
                possible_ean = str(GTIN(raw='{}'.format(possible_upc)))
                possible_eans.append(possible_ean)
                print('tried this: ',possible_ean)
                #requstte bulunmadan once database'e bak bu urun kayitli mi diye, eger bulursa stogu arttir. bulamazsan gunluk 100 limiti olan reques'ti calistir
                for possible_ean in possible_eans:
                    try:
                        #find the product in database and increase the quantity
                        product = Product.objects.get(ean2=possible_ean)
                        data['itemName'] = str(product)
                        data['itemQuantity'] = product.current_stock
                        return JsonResponse(data)
                    except:
                        data['itemName'] = 'Item not found'
                        data['itemQuantity'] = 'None'
                        return JsonResponse(data)
        else:
            data['itemName'] = 'Barcode invalid'
            data['itemQuantity'] = 'Barcode length less than 12'
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
            possible_eans = []
            if len(raw_number) >=14:
                possible_eans.append(str(convert_to_ean(raw_number[2:14])))
                possible_eans.append(str(convert_to_ean(raw_number[3:15])))
                # for i in range(len(raw_number)-11):
                #     possible_upc = raw_number[0+i:12+i]
                #     possible_ean = str(GTIN(raw='{}'.format(possible_upc)))
                #     print('tried this: ',possible_ean)

                #requstte bulunmadan once database'e bak bu urun kayitli mi diye, eger bulursa stogu arttir. bulamazsan gunluk 100 limiti olan reques'ti calistir
            elif len(raw_number) == 13:
                possible_eans.append(str(raw_number[1:13]))
            elif len(raw_number) == 12:
                possible_eans.append(str(convert_to_ean(raw_number)))
            else:
                print('string length in correnct: ',raw_number)
                data['result'] = 'invalid_barcode'
                return render(request, "increase.html", {"form": form})

            for possible_ean in possible_eans:
                possible_ean = str(GTIN(raw='{}'.format(possible_ean)))
                try:
                    #find the product in database and increase the quantity
                    product = Product.objects.get(ean2=possible_ean)
                    log = InventoryLog.objects.create(product=product, quantity=quantity)
                    print('item restocked:',possible_ean)
                    data['result'] = 'restocked'
                    data['itemName'] = str(product)
                    data['itemQuantity'] = product.current_stock
                    return JsonResponse(data)
                except:
                    pass
            print(possible_eans)
            #database'e bakti ve bulamadiysa hicbirsey return edemeycek ve sira bu limitli requesti calistirmaya gelecek    
            valid_eans = []
            for possible_ean in possible_eans:
                #time.sleep(0.5) #requesti yavaslatmak icin bir saniye koydum
                resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(possible_ean), headers=headers)
                #time.sleep(0.5) #requesti yavaslatmak icin bir saniye koydum
                data = json.loads(resp.text)
                if resp.status_code == 200 and data['total'] != 0:
                    #eger string icerisinde ikiden fazla valid ean varsa istenmeyen urunler de stoga girecek
                    valid_ean = possible_ean
                    print('valid ean: ', valid_ean)
                    valid_eans.append(valid_ean)
                else:
                    data['result'] = resp.status_code
                    print('response status code:',resp.status_code)
                    #return JsonResponse(data)
                
                
                
            print(valid_eans,'valid eands')
            #valid eanler saptandiktan sonra    
            #eger stringin icinde birden fazla valid ean varsa
            if not valid_eans: #eger listenin ici bossa
                print('listenin ici bos: ',valid_eans)
                data['result'] = 'restocked'
                data['itemName'] = 'valid ean ici bos'
                #data['itemQuantity'] = 'valid ean ici bos'
                return render(request, "increase.html", {"form": form})
            elif len(valid_eans) > 1:
                print('more than one valid eans in the string:',valid_eans)
                for ean in valid_eans:
                    print(ean)
                    brand = data['items'][0]['brand'] #burasi degisebilir eger upcitemdb kullanmazsam
                    if search('gildan',brand, IGNORECASE):
                        print('gildan valid eans: ',valid_eans)
                        if ean == raw_number[2:15]:
                            possible_gildan_ean = ean[2:15]
                            resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(ean), headers=headers)
                            if resp.status_code == 200 :
                                data = json.loads(resp.text)
                                for item in data['items']:
                                    brand, created = Brand.objects.get_or_create(name=item['brand'])
                                    model, created = Model.objects.get_or_create(brand=brand, name=item['model'])
                                    color, created = Color.objects.get_or_create(name=item['color'])
                                    size, created = Size.objects.get_or_create(name=item['size'])
                                    product = Product.objects.create(name=item['title'],model=model,color=color,size=size,ean2=item['ean'])
                                    log = InventoryLog.objects.create(product=product, quantity=quantity)
                                data['result'] = 'restocked'
                                data['itemName'] = str(product)
                                data['itemQuantity'] = product.current_stock
                            else:
                                data['result'] = 'restocked'
                                data['itemName'] = 'cannot find item'
                                print('cannot find item')
                        else:
                            data['result'] = 'restocked'
                            data['itemName'] = 'cannot find item'
                            print('cannot find item')
                        
                    elif search('bella',brand, IGNORECASE) or search('canvas',brand, IGNORECASE):
                        print('bella canvas valid eans: ',valid_eans)
                        if ean == raw_number[3:16]:
                            resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(ean), headers=headers)
                            if resp.status_code == 200 :
                                data = json.loads(resp.text)
                                for item in data['items']:
                                    brand, created = Brand.objects.get_or_create(name=item['brand'])
                                    model, created = Model.objects.get_or_create(brand=brand, name=item['model'])
                                    color, created = Color.objects.get_or_create(name=item['color'])
                                    size, created = Size.objects.get_or_create(name=item['size'])
                                    product = Product.objects.create(name=item['title'],model=model,color=color,size=size,ean2=item['ean'])
                                    log = InventoryLog.objects.create(product=product, quantity=quantity)
                                data['result'] = 'restocked'
                                data['itemName'] = str(product)
                                data['itemQuantity'] = product.current_stock
                            else:
                                data['result'] = 'restocked'
                                data['itemName'] = 'cannot find item'
                                print('cannot find item')
                        else:
                            data['result'] = 'restocked'
                            data['itemName'] = 'cannot find item'
                            print('cannot find item')
                    else:
                        #eger birden fazla valid ean var ve bella veya gildan oldugu saptanamiyprsa hic birsey yapma ve sayfayi yeniden ac
                        return render(request, "increase.html", {"form": form})
                return render(request, "increase.html", {"form": form})
            else: #yoksa kalsik metodtan devam
                resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(valid_eans[0]), headers=headers)
                data = json.loads(resp.text)
                for item in data['items']:
                    brand, created = Brand.objects.get_or_create(name=item['brand'])
                    model, created = Model.objects.get_or_create(brand=brand, name=item['model'])
                    color, created = Color.objects.get_or_create(name=item['color'])
                    size, created = Size.objects.get_or_create(name=item['size'])
                    product = Product.objects.create(name=item['title'],model=model,color=color,size=size,ean2=item['ean'])
                    log = InventoryLog.objects.create(product=product, quantity=quantity)  
                print("new item created and stocked: ", valid_eans[0])
                data['result'] = 'restocked'
                data['itemName'] = str(product)
                data['itemQuantity'] = product.current_stock
                return JsonResponse(data)
        else:
            data['result'] = 'restocked'
            data['itemName'] = 'cannot find item'
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
            possible_eans = []
            if len(raw_number) >=14:
                possible_eans.append(str(convert_to_ean(raw_number[2:14])))
                possible_eans.append(str(convert_to_ean(raw_number[3:15])))
                # for i in range(len(raw_number)-11):
                #     possible_upc = raw_number[0+i:12+i]
                #     possible_ean = str(GTIN(raw='{}'.format(possible_upc)))
                #     print('tried this: ',possible_ean)

                #requstte bulunmadan once database'e bak bu urun kayitli mi diye, eger bulursa stogu arttir. bulamazsan gunluk 100 limiti olan reques'ti calistir
            elif len(raw_number) == 13:
                possible_eans.append(str(raw_number[1:13]))
            elif len(raw_number) == 12:
                possible_eans.append(str(convert_to_ean(raw_number)))
            else:
                print('string length in correnct: ',raw_number)
                data['result'] = 'invalid_barcode'
                return JsonResponse(data)

            #requstte bulunmadan once database'e bak bu urun kayitli mi diye, eger bulursa stogu arttir. bulamazsan gunluk 100 limiti olan reques'ti calistir
            for possible_ean in possible_eans:
                try:
                    #find the product in database and increase the quantity
                    product = Product.objects.get(ean2=possible_ean)
                    log = InventoryLog.objects.create(product=product, quantity=quantity)
                    print('item sold:',possible_ean)
                    data['result'] = 'sold'
                    data['itemName'] = str(product)
                    data['itemQuantity'] = product.current_stock
                    return JsonResponse(data)
                except:
                    data['result'] = 'not_found'
                    data['itemName'] = 'item does not exist'
                    data['itemQuantity'] = 'not found'
                    return JsonResponse(data)

        else:
            print('form is not valid')
            return render(request, "decrease.html", {"form": form})
    else:
        print('no post or ajax request')
        return render(request, "decrease.html", {"form": form})

class ProductDetailView(generic.DetailView):
    model = Product



