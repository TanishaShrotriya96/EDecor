from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
# Create your views here.
def home(request):

    t = get_template('home.html')
    html = t.render({'prediction': 'hi'})
    return HttpResponse(html)
    #return HttpResponse("You're looking at question %s.")

def index(request):

    t = get_template('index.html')
    html = t.render({'prediction': 'hi'})
    return HttpResponse(html)
    #return HttpResponse("You're looking at question %s.")
