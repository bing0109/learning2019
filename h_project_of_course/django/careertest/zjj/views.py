from django.shortcuts import render

# Create your views here.
def company(request):
    return render(request,'zjj/company.html')
def index(request):
    return render(request,'zjj/index.html')
def demo(request):
    return render(request,'zjj/demo.html')
def index2(request):
    return render(request,'zjj/index2.html')