from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from .forms import WordForm

import requests
from django.utils import simplejson
from django.core.context_processors import csrf


def index(request):
    current_data = requests.get("https://api.myjson.com/bins/2csub").json()
    pri_words = []
    priority_data = requests.get("https://api.myjson.com/bins/3ddib").json()
    for word in priority_data:
        pri_words.append(word.upper().encode('ascii', 'ignore'))
    args = {}
    args.update(csrf(request))
    args['pri'] = pri_words
    args['words'] = current_data
    return render_to_response('words.html', args)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def create(request):
    if request.POST:
        form = WordForm(request.POST)
        if form.is_valid():
            pri_words = []
            priority_data = requests.get("https://api.myjson.com/bins/3ddib").json()
            for word in priority_data:
                pri_words.append(word.upper().encode('ascii', 'ignore'))
            pri_words.insert(0, form.cleaned_data['word'].upper())
            headers = {'Content-type': 'application/json'}
            response = requests.put("https://api.myjson.com/bins/3ddib", data=simplejson.dumps(pri_words), headers=headers)
            return HttpResponseRedirect('Words')            
    else:
        form = WordForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('add_word.html', args)
