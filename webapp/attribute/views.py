import os
import re
import shutil

import datetime
import xlrd
from django.http import HttpResponse
from django.shortcuts import render

from webapp.models import *
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *


from django.http import HttpResponse
from django.shortcuts import render


def index(request, template_name):

    return render(request, template_name)


def jump(request, template_name):

    return render(request, template_name)



