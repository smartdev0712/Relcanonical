from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'script/index.html')

def php(request):
    return render(request, 'script/php.html')