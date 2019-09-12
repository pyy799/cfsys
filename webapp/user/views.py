from django.http import HttpResponse
from django.shortcuts import render


def index(request, template_name):

    return render(request, template_name)


def jump(request, template_name):

    return render(request, template_name)