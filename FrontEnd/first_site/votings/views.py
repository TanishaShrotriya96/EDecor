from django.shortcuts import render
from django.views.generic import TemplateView, ListView # Import TemplateView
from django.http import HttpResponse
#from .model import bed

# Add the two views we have been talking about  all this time :)
class IndexPageView(TemplateView):
    template_name = "polls/index.html"


class CatPageView(TemplateView):
    template_name = "polls/cat.html"








'''#from django.shortcuts import render
#from django.template.loader import get_template
# Create your views here.
#from django.http import HttpResponse


#def index(request):
 #   return HttpResponse("Hello, world. You're at the polls index.")

#def basefunc(request):
#	b = get_template('polls/login.html')
#	html = b.render({'shubhangi':'hi'})
#	return HttpResponse(html)
    #return HttpResponse("Hello, world. You're at the polls index.")'''


