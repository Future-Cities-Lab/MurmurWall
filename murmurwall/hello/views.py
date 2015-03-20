from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from .forms import WordForm

import requests
from django.utils import simplejson
from django.core.context_processors import csrf

pri_words = []

def index(request):
    current_data = requests.get("https://api.myjson.com/bins/2csub").json()
    # related_terms_list = []
    # for trend in current_data:
    #     for related_term in current_data[trend]["Top searches for"]:
    #         term = related_term.upper().encode('ascii', 'ignore')
    #         if term not in related_terms_list:
    #             related_terms_list.append(term)

    if len(pri_words) is 0:
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
