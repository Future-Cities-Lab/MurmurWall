from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

import requests
from django.utils import simplejson

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    current_data = requests.get("https://api.myjson.com/bins/2csub")
    return HttpResponse(simplejson.dumps(current_data.json()), content_type="application/json")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

