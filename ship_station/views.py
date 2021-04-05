from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from .forms import FileForm
from .models import File
import pandas as pd

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


