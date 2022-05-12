from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    msg = 'test'
    return render(request, 'index.html', {'message' : msg})

def create(request):
    return HttpResponse('create')

def read(request, id):
    return HttpResponse('Read' + id)

def result(request):
    username = request.POST['username']
    body_dict = {
        "username" : username,
        "key" : 123456
    }
    url = 'http://101.101.218.250:30005/'
    res = requests.post(url, json=body_dict)

    return HttpResponse(res)