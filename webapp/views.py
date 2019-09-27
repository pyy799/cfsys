from django.http import HttpResponse
from django.shortcuts import render

from webapp.upattribute import import_attribute


def index(request, template_name):
    # import_attribute()
    return render(request, template_name)


def jump(request, template_name):

    return render(request, template_name)
