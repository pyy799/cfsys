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
from webapp.utils.query import get_query, create_data
from django.views.decorators.csrf import csrf_exempt


from django.http import HttpResponse
from django.shortcuts import render
from webapp.models import *
from webapp.upattribute import import_attribute

from django.contrib.auth.decorators import login_required
from webapp.shortcuts.decorator import permission_required

# 增加大小类、属性列表显示
@login_required
@permission_required('webapp.product_attribute_management')
def index(request,template_name):
    # attibute_list = Attribute
    # t = Attribute
    # import_attribute()
    attributes = Attribute.objects.all()
    # result = {}
    if request.method == "POST":
        attribute = request.POST.get("attribute_add")
        first_class = request.POST.get("first_class_add")
        second_class = request.POST.get("second_class_add", None)
        meaning = request.POST.get("meaning_add")
        information = request.POST.get("information_add", None)
        if second_class:
            ACT = 't'
        else:
            ACT = 'c'
        attr = Attribute.objects.create(ACT=ACT,attribute=attribute,first_class=first_class,second_class=second_class,meaning=meaning,information=information)
        attr.save()
    return render(request,template_name,{'attributes': attributes})

     #    if attribute != None and first_class != None:
     #        if  second_class == None:
     #            ACT='c'
     #        elif second_class !=None:
     #            ACT='t'
     #        attr = Attribute.objects.create(ACT=ACT,attribute=attribute,first_class=first_class,second_class=second_class,meaning=meaning,information=information)
     #        attr.save()
     #        result['statu'] = 'success'
     #    else:
     #        result['statu'] = 'error'
     #
     # return render(request,template_name,{'attributes': attributes,"result":result})




def jump(request,template_name):
    return render(request, template_name)

# 修改大小类
def edit_attr(request):
    return render(request)

#删除属性
def del_class(request,delete_id):
    # Attribute.objects.filter(id=delete_id).delete()
    return render(request)

# @csrf_exempt
# def attribute_infor(request):
#     fil = {"ACT": AttributeType.A, "is_vaild": True}
#     attribute_list, count, error= get_query(request, Attribute, **fil)
#     res = create_data(request.POST.get("draw", 1), attribute_list, count)
#     return HttpResponse(res)
