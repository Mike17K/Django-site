from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from matplotlib.pyplot import show, table
from main.models import Table
from .models import Table,Canvas
from .forms import CreateNewCanvas, CreateNewTable

# Create your views here.

def index(response):
    return render(response, 'main/index.html',{})

def aboutUs(response):
    return render(response, 'main/aboutUs.html',{})

def contactUs(response):
    return render(response, 'main/contactUs.html',{})

def gallery(response):
    c = Canvas.objects.filter(show=1)
    return render(response, 'main/gallery.html',{"c":c})

def createCanvas(response):    
    if response.method == 'POST':
        form = CreateNewCanvas(response.POST,response.FILES)
        if form.is_valid():
            cnv = Canvas()
            cnv.txt = form.cleaned_data['name']
            cnv.image = form.cleaned_data['image']
            cnv.show = form.cleaned_data['show']
            cnv.save()
            
        #return HttpResponseRedirect("/%i" %t.id)
        return render(response, 'main/index.html',{})
    else:
        form = CreateNewCanvas()

    return render(response, 'main/createCanvas.html',{"form":form})

def createTable(response):
    if response.method == 'POST':
        form = CreateNewTable(response.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            t = Table(name=n)
            t.save()
            
            response.user.table.add(t)
            
        #return HttpResponseRedirect("/%i" %t.id)
        return render(response, 'main/index.html',{})
    else:
        form = CreateNewTable()

    return render(response, 'main/createTable.html',{"form":form})



'''
def index(response,id):
    ls = Table.objects.get(id=id)

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c"+str(item.id))== 'clicked':
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")

    return render(response,'main/list.html',{'ls':ls})'''