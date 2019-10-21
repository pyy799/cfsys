import os
import re
import shutil

import datetime
import xlrd
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render

from webapp.models import *
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *
from webapp.utils.query import get_query, create_data
from django.views.decorators.csrf import csrf_exempt


from webapp.upattribute import import_attribute

from django.contrib.auth.decorators import login_required
from webapp.shortcuts.decorator import permission_required
from django.db.models import Q
from django.contrib import messages

# 属性列表显示
@login_required
@permission_required('webapp.product_attribute_management')
def index(request,template_name):
    attributes = Attribute.objects.all()
    return render(request,template_name,{'attributes': attributes})

# 增加大小类
@login_required
@permission_required('webapp.product_attribute_management')
def add_attribute(request):
    attribute = request.POST.get("attribute_add")
    first_class = request.POST.get("first_class_add")
    second_class = request.POST.get("second_class_add", None)
    meaning = request.POST.get("meaning_add")
    information = request.POST.get("information_add", None)
    if second_class:
        ACT = 't'
    else:
        ACT = 'c'

    attr = Attribute.objects.create(ACT=ACT, attribute=attribute, first_class=first_class,second_class=second_class, meaning=meaning, information=information)
    attr.save()
    return HttpResponseRedirect("/attribute/page_attribute/")

    # 验重、判空
    # if meaning !='':
    #     check_meaning = Attribute.objects.filter(meaning=meaning)
    #     if check_meaning == []:
    #         if second_class:
    #             ACT = 't'
    #             check_second = Attribute.objects.filter(second_class=second_class)
    #             if check_second == []:
    #                 attr = Attribute.objects.create(ACT=ACT, attribute=attribute, first_class=first_class,
    #                                                 second_class=second_class, meaning=meaning, information=information)
    #                 attr.save()
    #             else:
    #                 messages.success(request,"已有此分类")
    #         else:
    #             ACT = 'c'
    #             check_first = Attribute.objects.filter(first_class=first_class)
    #             if check_first == []:
    #                 attr = Attribute.objects.create(ACT=ACT, attribute=attribute, first_class=first_class,
    #                                                 second_class=second_class, meaning=meaning, information=information)
    #                 attr.save()
    #             else:
    #                 print(0)
    #     else:
    #         print(0)
    # else:
    #     print(1)
    # return HttpResponseRedirect("/attribute/page_attribute/")


def jump(request,template_name):
    return render(request, template_name)

# 修改属性
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def attribute_edit(request):
    attribute_id = request.POST.get("attribute_id")
    information =request.POST.get("information_edit")
    # print(attribute_id)
    attribute = Attribute.objects.filter(id=attribute_id).first()
    if attribute:
        attribute.information = information
        attribute.save()

    # print(attribute.information)
    # p=Product.objects.get(id=99)
    # # p1=p.pack_data()
    # a=p.maturity_id
    # c = Product.objects.filter(maturity_id='3')
    # print(a)
    return JsonResponse({"status": 0})

# 修改大小类
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def class_edit(request):
    # attr_class = Attribute.objects.filter(Q(id=class_id), Q(ACT=class_act)).first()
    # ex_first = attr_class.first_class
    # attr_class.first_class = first_class_edit
    # attr_class.second_class = second_class_edit
    # attr_class.meaning = class_meaning
    # attr_class.information = class_information
    # attr_class.save()
    # if class_act == 'c':
    #     attr_c = Attribute.objects.filter(Q(first_class=ex_first), Q(ACT='t'))
    #     for attr in attr_c:
    #         attr.first_class=first_class_edit
    #         attr.save()
    # # return JsonResponse({"first": first_class_edit})
    # return JsonResponse({"status": 0})

    class_id = request.POST.get("class_id")
    class_act = request.POST.get("class_act")
    # class_attribute =request.POST.get("class_attribute")
    first_class_edit = request.POST.get("first_class_edit")
    second_class_edit = request.POST.get("second_class_edit")
    class_meaning = request.POST.get("class_meaning")
    class_information =request.POST.get("class_information")

    attr_class = Attribute.objects.filter(Q(id=class_id), Q(ACT=class_act)).first()
    ex_first = attr_class.first_class
    attr_class.information = class_information

    status0 = 1
    status1 = 1
    status2 = 1
    if first_class_edit:
        status0 = 0
        attr_class.first_class = first_class_edit
        if class_meaning:
            status1 = 0
            attr_class.meaning = class_meaning
            if class_act == 't':
                if second_class_edit:
                    status2 = 0
                    attr_class.second_class=second_class_edit
                    attr_class.save()
                else:
                    return JsonResponse({"status0": status0, "status1": status1, "status2": status2})
            elif class_act == 'c':
                attr_class.second_class = second_class_edit
                attr_c = Attribute.objects.filter(Q(first_class=ex_first), Q(ACT='t'))
                for attr in attr_c:
                    attr.first_class = first_class_edit
                    # attr.second_class=second_class_edit
                    attr.save()
                attr_class.save()
        else:
            return JsonResponse({"status0": status0, "status1": status1, "status2": status2})
    else:
        return JsonResponse({"status0": status0, "status1": status1, "status2": status2})

    return JsonResponse({"status0": status0,"status1": status1,"status2": status2})


# 删除大小类(查询产品)
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def delete_class(request):
    id = request.GET.get("id")
    act = request.GET.get("act")
    first_class = request.GET.get("first_class")
    count=0
    id_s=[]
    #判断大小类
    if act == 'c':
        attr_s = Attribute.objects.filter(first_class=first_class)
        for attr in attr_s:
            id_s.append(attr.id)
        for id in id_s:
            p=Product.objects.filter(
                Q(maturity__id=id) | Q(business__id=id) | Q(independence__id=id) | Q(technology__id=id))
            count = count+len(p)
    # print(p)
    elif act == 't':
        id_s.append(id)
        p=Product.objects.filter(
            Q(maturity__id=id) | Q(business__id=id) | Q(independence__id=id) | Q(technology__id=id))
        count = count+len(p)
    # count = len(p)
    print(count)
    return JsonResponse({"count":count,"id_s":id_s})

# 删除大小类(查询产品)
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def godelete_class(request):
    delete_id=request.GET.get("delete_id")
    delete_count = request.GET.get("delete_count")
    print(delete_id)
    # print(delete_count)
    id_s=re.split(',',delete_id)
    if delete_count == '0':
        for id in id_s:
            Attribute.objects.filter(id=id).delete()
    return JsonResponse({"status": 0})