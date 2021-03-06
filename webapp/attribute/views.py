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

    page_dict = {}
    maturity = Attribute.objects.filter(attribute='M').order_by('first_class','second_class')
    independence = Attribute.objects.filter(attribute='I').order_by('first_class','second_class')

    business = Attribute.objects.filter(attribute='B').order_by('first_class','second_class')

    technology = Attribute.objects.filter(attribute='T').order_by('first_class','second_class')

    page_dict.update({"maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
    return render(request, template_name, page_dict)

# 增加大小类
@login_required
@permission_required('webapp.product_attribute_management')
def add_attribute(request):
    attribute = request.POST.get("attribute_add")
    first_class = request.POST.get("first_class_add")
    second_class = request.POST.get("second_class_add", None)
    meaning = request.POST.get("meaning_add")
    information = request.POST.get("information_add", None)

    # first_class=first_class.strip()
    # second_class=second_class.strip()
    # meaning=meaning.strip()
    # information=information.strip()

    first_class=first_class.replace("\n", "").replace(' ','')
    second_class=second_class.replace("\n", "").replace(' ','')
    meaning=meaning.replace("\n", "").replace(' ','')
    information=information.replace("\n", "").replace(' ','')

    # check_meaning = Attribute.objects.filter(meaning=meaning)
    # if len(check_meaning) == 0:
    if meaning:
        if first_class:
            if second_class:
                act = 't'
                # all_first = Attribute.objects.filter(Q(first_class=first_class),Q(ACT='c'))
                check_meaning = Attribute.objects.filter(Q(meaning=meaning),Q(attribute=attribute),Q(first_class=first_class),Q(ACT='t'))
                check_first = Attribute.objects.filter(Q(first_class=first_class), Q(attribute=attribute),Q(ACT='c'))
                check_second = Attribute.objects.filter(Q(second_class=second_class), Q(attribute=attribute),Q(ACT='t'))
                if check_first:
                    if len(check_second) == 0:
                        if len(check_meaning)==0:
                            attr = Attribute.objects.create(ACT=act, attribute=attribute, first_class=first_class,
                                                            second_class=second_class, meaning=meaning, information=information)
                            attr.save()
                            messages.success(request, "增加成功")
                        else:
                            messages.error(request, "已有此含义，请重新输入！")
                    else:
                        messages.error(request, "已有此小类，请重新输入！")
                else:
                    messages.error(request, "此属性中无此大类，请重新输入或先增加此大类！")

            else:
                act = 'c'
                check_meaning = Attribute.objects.filter(Q(meaning=meaning),Q(attribute=attribute),Q(ACT='c'))
                check_first = Attribute.objects.filter(Q(first_class=first_class),Q(attribute=attribute),Q(ACT='c'))
                if len(check_first) == 0:
                    if len(check_meaning)==0:
                        attr = Attribute.objects.create(ACT=act, attribute=attribute, first_class=first_class,
                                                        second_class=second_class, meaning=meaning, information=information)
                        attr.save()
                        messages.success(request, "增加成功")
                    else:
                        messages.error(request, "已有此含义，请重新输入！")
                else:
                    messages.error(request, "已有此大类，请重新输入！")
        else:
            messages.error(request, "大类不能为空，请重新输入！")
    else:
        messages.error(request, "含义不能为空，请重新输入！")

    # else:
    #     messages.success(request, "已有此含义，请重新输入！")

    return HttpResponseRedirect("/attribute/page_attribute/"+ attribute)



def jump(request,template_name):
    return render(request, template_name)

# 修改属性
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def attribute_edit(request):
    attribute_id = request.POST.get("attribute_id")
    information =request.POST.get("information_edit")
    # information = information.replace("\n", "")
    information=information.replace("\n", "").strip()

    # print(attribute_id)
    attribute = Attribute.objects.filter(id=attribute_id).first()
    if attribute:
        if attribute.information==information:
            status=1
        else:
            attribute.information = information
            attribute.save()
            status=0
    else:
        status=2
    # print(attribute.information)
    # p=Product.objects.get(id=99)
    # # p1=p.pack_data()
    # a=p.maturity_id
    # c = Product.objects.filter(maturity_id='3')
    # print(a)
    return JsonResponse({"status": status})

# 修改大小类
@csrf_exempt
@login_required
@permission_required('webapp.product_attribute_management')
def class_edit(request):

    class_id = request.POST.get("class_id")
    class_act = request.POST.get("class_act")
    class_attribute =request.POST.get("class_attribute")
    first_class_edit = request.POST.get("first_class_edit")
    second_class_edit = request.POST.get("second_class_edit")
    class_meaning = request.POST.get("class_meaning")
    class_information =request.POST.get("class_information")

    # first_class_edit=first_class_edit.strip()
    # second_class_edit=second_class_edit.strip()
    # class_meaning=class_meaning.strip()
    # class_information=class_information.strip()
    first_class_edit=first_class_edit.replace("\n", "")
    second_class_edit=second_class_edit.replace("\n", "")
    class_meaning=class_meaning.replace("\n", "")
    class_information=class_information.replace("\n", "")

    attr_class = Attribute.objects.filter(Q(id=class_id), Q(ACT=class_act), Q(attribute=class_attribute)).first()
    ex_first = attr_class.first_class
    ex_second=attr_class.second_class
    ex_meaning=attr_class.meaning
    ex_information=attr_class.information
    attr_class.information = class_information
    if ex_first==first_class_edit and ex_second==second_class_edit and ex_meaning==class_meaning and ex_information==class_information:
        status0=3
        return JsonResponse({"status0": status0})
    else:
        if first_class_edit:
            if class_meaning:
                # all_meaning = Attribute.objects.filter(Q(meaning=class_meaning), ~Q(id=class_id))
                if class_act == 't':
                    if second_class_edit:
                        all_meaning = Attribute.objects.filter(Q(meaning=class_meaning), ~Q(id=class_id), Q(ACT='t'), Q(attribute=class_attribute), Q(first_class=first_class_edit))
                        all_second = Attribute.objects.filter(Q(second_class=second_class_edit), Q(ACT='t'), Q(attribute=class_attribute), Q(first_class=first_class_edit), ~Q(id=class_id))
                        if len(all_meaning)==0 and len(all_second)==0:
                            status0 = 0
                            status1 = 0
                            attr_class.second_class = second_class_edit
                            attr_class.meaning = class_meaning
                            attr_class.save()
                            return JsonResponse({"status0": status0})
                            # return JsonResponse({"status0": status0, "status1": status1})
                            # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})

                        else:
                            status0 = 1
                            status1 = 1
                            return JsonResponse({"status0": status0})
                            # return JsonResponse({"status0": status0, "status1": status1})
                            # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})
                    else:
                        status0 = 2
                        status1 = 0
                        return JsonResponse({"status0": status0})
                        # return JsonResponse({"status0": status0, "status1": status1})
                        # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})
                elif class_act == 'c':
                    all_meaning = Attribute.objects.filter(Q(meaning=class_meaning), ~Q(id=class_id), Q(ACT='c'), Q(attribute=class_attribute))
                    all_first = Attribute.objects.filter(Q(first_class=first_class_edit), Q(ACT='c'), Q(attribute=class_attribute), ~Q(id=class_id))
                    if len(all_first) == 0 and len(all_meaning) == 0:
                        status0 = 0
                        status1 = 0
                        attr_class.first_class = first_class_edit
                        attr_class.meaning = class_meaning
                        attr_c = Attribute.objects.filter(Q(first_class=ex_first), Q(ACT='t'))
                        for attr in attr_c:
                            attr.first_class = first_class_edit
                            attr.save()
                        attr_class.save()
                        return JsonResponse({"status0": status0})
                        # return JsonResponse({"status0": status0, "status1": status1})
                        # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})
                    else:
                        status0 = 1
                        status1 = 1
                        return JsonResponse({"status0": status0})
                        # return JsonResponse({"status0": status0, "status1": status1})
                        # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})
            else:
                status0 = 2
                status1 = 0
                return JsonResponse({"status0": status0})
                # return JsonResponse({"status0": status0, "status1": status1})
                # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})
        else:
            status0 = 2
            status1 = 0
            return JsonResponse({"status0": status0})
            # return JsonResponse({"status0": status0, "status1": status1})
            # return JsonResponse({"status0": status0, "status1": status1, "status2": 0})


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
    id_s.append(id)
    #判断大小类
    if act == 'c':
        attr_s = Attribute.objects.filter( Q(first_class=first_class),Q(ACT='t'))
        for attr in attr_s:
            id_s.append(attr.id)
        for id in id_s:
            p=Product.objects.filter(
                Q(maturity__id=id) | Q(business__id=id) | Q(independence__id=id) | Q(technology__id=id))
            count = count+len(p)
    # print(p)
    elif act == 't':
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