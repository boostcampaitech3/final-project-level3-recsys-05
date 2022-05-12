from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def index(request):
    msg = 'test'
    return render(request, 'index.html', {'message' : msg})

def create(request):
    return HttpResponse('create')

def read(request, id):
    return HttpResponse('Read' + id)

def result(request):
    result = request.POST['username']
    return HttpResponse(result)