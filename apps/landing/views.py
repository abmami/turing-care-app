from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


# Create your views here.
def index(request):
    context = {'segment': 'landing'}

    html_template = loader.get_template('landing/index.html')
    return HttpResponse(html_template.render(context, request))