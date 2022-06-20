from django.http import HttpResponse
from django.shortcuts import render
import requests
import logging

logger = logging.getLogger('products')
# Create your views here.
def index(request):
    msg = 'test'
    return render(request, 'index.html', {'message' : msg})

def create(request):
    return HttpResponse('create')

def read(request, id):
    return HttpResponse('Read' + id)

def nologin(request):
    username = request.GET['username']
    body_dict = {
        "username" : username,
        "key" : 123456
    }
    url = 'http://101.101.218.250:30005/'
    res = requests.post(url, json=body_dict)
    res_dict = res.json()
    non_filtering_output = res_dict['non_filtering_output']
    lately_filtering_output = res_dict['lately_filtering_output']
    total_filtering_output = res_dict['total_filtering_output']

    data = {
        'username': username,
        'non_filtering_output': non_filtering_output,
        'lately_filtering_output': lately_filtering_output,
        'total_filtering_output': total_filtering_output
    }
    logger.info(f'{username} gets nologin service')

    return render(request, 'nologin-result.html', data)