# coding=utf-8
import os
import re
import operator

from cfsys.settings import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webapp.models import *
from webapp.utils.query import get_query, create_data


def index(request, template_name):
    """
    查询/展示 页面
    """
    page_dict = {}
    pCompany = COMPANY_CHOICE
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1)
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2)
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3)
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4)

    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
    return render(request, template_name, page_dict)


def jump(request, template_name):
    return render(request, template_name)


@csrf_exempt
# 查询页签数据
def search(request):
    # fil = {"status": ProductStatus.PASS,"is_vaild": True}
    fil = {"status": ProductStatus.PASS,"is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 展示页面数据
def show(request, template_name):
    page_dict = {}
    pCompany = COMPANY_CHOICE
    # 属性大类查询
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('-first_class')
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('-first_class')
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3).order_by('first_class')
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4).order_by('first_class')
    # 属性列表
    maturity_list = []
    independence_list = []
    business_list = []
    technology_list = []
    # 属性列表剪切后
    maturity_list1 = []
    independence_list1 = []
    business_list1 = []
    # 查询结果
    maturity_product = {}
    maturity_product1 = []
    independence_product = {}
    independence_product1 = []
    business_product_list = []
    business_product = {}
    business_product1 = []
    technology_product = {}
    technology_product1 = []
    # 查询条件
    maturity_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    independence_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    business_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    technology_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    maturity_independence_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    business_technology_search_dict = {"status": ProductStatus.PASS, "is_vaild": True}

    p1 = re.compile(r'[(or（](.*?)[)or）]', re.S)  # 取（）内文字
    # 成熟度
    for i in maturity:
        maturity_search_dict.update({"maturity__first_class":i.first_class})
        product_list = Product.objects.filter(**maturity_search_dict)
        num = len(product_list)
        name_m = re.findall(p1, i.meaning)
        if name_m:
            maturity_list1.append(name_m[0])
        else:
            maturity_list1.append(i.meaning)
        maturity_list.append(i.meaning)
        maturity_product.update({i.meaning: num})
        maturity_product1.append({"name": i.meaning, "value": num})
    # 自主度
    for i in independence:
        independence_search_dict.update({"independence__first_class":i.first_class})
        product_list = Product.objects.filter(**independence_search_dict)
        num = len(product_list)
        name_i = re.findall(p1, i.meaning)
        if (name_i):
            independence_list1.append(name_i[0])
        else:
            independence_list1.append(i.meaning)
        independence_list.append(i.meaning)
        independence_product.update({i.meaning: num})
        independence_product1.append({"name": i.meaning, "value": num})
    # 业务领域
    for i in business:
        business_search_dict.update({"business__first_class":i.first_class})
        product_list = Product.objects.filter(**business_search_dict)
        num = len(product_list)
        business_list.append(i.meaning)
        business_list1.append(i.meaning.strip('业务大类'))
        business_product.update({i.meaning: num})
        business_product1.append({"name": i.meaning, "value": num})
        business_product_list.append([i.meaning, product_list])
    # 技术形态
    for i in technology:
        technology_search_dict.update({"technology__first_class":i.first_class})
        product_list = Product.objects.filter(**technology_search_dict)
        technology_list.append(i.meaning)
        num = len(product_list)
        technology_product.update({i.meaning: num})
        technology_product1.append({"name": i.meaning, "value": num})

    # 成熟度-自主度
    num1 = 0
    num2 = 0
    maturity_independence_max_num = 0
    maturity_independence = []
    for ind in independence:
        for mat in maturity:
            maturity_independence_search_dict.update({"maturity__first_class": mat.first_class,
                                          "independence__first_class": ind.first_class})
            maturity_independence_product_list = Product.objects.filter(**maturity_independence_search_dict)
            num3 = len(maturity_independence_product_list)
            maturity_independence_max_num=max(maturity_independence_max_num,num3)
            maturity_independence_one = [num1, num2, num3]
            num2 += 1
            maturity_independence.append(maturity_independence_one)
        num1 += 1
        num2 = 0

    # 业务领域-技术形态
    num4 = 0
    num5 = 0
    business_technology_max_num=0
    business_technology = []
    for tec in technology:
        for bus in business:
            business_technology_search_dict.update({"business__first_class": bus.first_class,
                                        "technology__first_class": tec.first_class})
            business_technology_product_list = Product.objects.filter(**business_technology_search_dict)
            num6 = len(business_technology_product_list)
            business_technology_max_num=max(business_technology_max_num,num6)
            business_technology_one = [num4, num5, num6]
            num5 += 1
            business_technology.append(business_technology_one)
        num4 += 1
        num5 = 0
    # 前端返回值
    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology,
                      "maturity_list": maturity_list, "independence_list": independence_list,
                      "business_list": business_list, "technology_list": technology_list,
                      "maturity_list1": maturity_list1, "independence_list1": independence_list1,
                      "business_list1": business_list1,
                      "maturity_product1": maturity_product1,
                      "independence_product1": independence_product1,
                      "business_product1": business_product1,
                      "technology_product1": technology_product1,
                      "maturity_independence": maturity_independence,
                      "business_technology": business_technology,
                      "maturity_independence_max_num":maturity_independence_max_num,
                      "business_technology_max_num":business_technology_max_num

                      })
    return render(request, template_name, page_dict)


# 展示页-查询展示
def search_show(request, template_name):
    pCompany = COMPANY_CHOICE
    page_dict = {}
    # 接收前端数据
    check_box_list = request.POST.getlist('check_box_list')
    maturity_choice = request.POST.get('maturity__first_class')
    independence_choice = request.POST.get('independence__first_class')
    business_choice = request.POST.get('business__first_class')
    technology_choice = request.POST.get('technology__first_class')
    search_dict = {"status": ProductStatus.PASS, "is_vaild": True}
    if check_box_list:
        search_dict["pCompany__in"] = check_box_list
    if maturity_choice:
        search_dict["maturity__first_class"] = maturity_choice
    if independence_choice:
        search_dict["independence__first_class"] = independence_choice
    if business_choice:
        search_dict["business__first_class"] = business_choice
    if technology_choice:
        search_dict["technology__first_class"] = technology_choice

    # product_list = Product.objects.filter(**search_dict)
    # 属性大类查询
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('-first_class')
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('-first_class')
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3).order_by('first_class')
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4).order_by('first_class')
    # 属性列表
    maturity_list = []
    independence_list = []
    business_list = []
    technology_list = []
    # 属性列表剪切后
    maturity_list1 = []
    independence_list1 = []
    business_list1 = []
    # 查询结果
    maturity_product = {}
    maturity_product1 = []
    independence_product = {}
    independence_product1 = []
    business_product_list = []
    business_product = {}
    business_product1 = []
    technology_product = {}
    technology_product1 = []
    # print(search_dict)
    # 查询条件
    maturity_search_dict = {}
    independence_search_dict = {}
    business_search_dict = {}
    technology_search_dict = {}
    maturity_independence_search_dict = {}
    business_technology_search_dict = {}
    maturity_search_dict.update(search_dict)
    independence_search_dict.update(search_dict)
    business_search_dict.update(search_dict)
    technology_search_dict.update(search_dict)
    maturity_independence_search_dict.update(search_dict)
    business_technology_search_dict.update(search_dict)

    p1 = re.compile(r'[(or（](.*?)[)or）]', re.S)  # 取（）内文字
    # 成熟度
    if maturity_choice:
        for i in maturity:
            if maturity_choice == i.first_class:
                product_list = Product.objects.filter(**maturity_search_dict)
                num = len(product_list)
            else:
                num = 0
            maturity_list.append(i.meaning)
            name_m = re.findall(p1, i.meaning)
            if (name_m):
                maturity_list1.append(name_m[0])
            else:
                maturity_list1.append(i.meaning)
            maturity_product.update({i.meaning: num})
            maturity_product1.append({"name": i.meaning, "value": num})
    else:
        for i in maturity:
            maturity_search_dict.update({"maturity__first_class": i.first_class})
            product_list = Product.objects.filter(**maturity_search_dict)
            num = len(product_list)
            maturity_list.append(i.meaning)
            name_m = re.findall(p1, i.meaning)
            if (name_m):
                maturity_list1.append(name_m[0])
            else:
                maturity_list1.append(i.meaning)
            maturity_product.update({i.meaning: num})
            maturity_product1.append({"name": i.meaning, "value": num})
            print(maturity_search_dict)

    # 自主度
    if independence_choice:
        for i in independence:
            if independence_choice == i.first_class:
                product_list = Product.objects.filter(**independence_search_dict)
                num = len(product_list)
            else:
                num = 0
            independence_list.append(i.meaning)
            name_i = re.findall(p1, i.meaning)
            if (name_i):
                independence_list1.append(name_i[0])
            else:
                independence_list1.append(i.meaning)
            independence_product.update({i.meaning: num})
            independence_product1.append({"name": i.meaning, "value": num})
    else:
        for i in independence:
            independence_search_dict.update({"independence__first_class": i.first_class})
            product_list = Product.objects.filter(**independence_search_dict)
            num = len(product_list)
            independence_list.append(i.meaning)
            name_i = re.findall(p1, i.meaning)
            if (name_i):
                independence_list1.append(name_i[0])
            else:
                independence_list1.append(i.meaning)
            independence_product.update({i.meaning: num})
            independence_product1.append({"name": i.meaning, "value": num})

    # 业务领域
    if business_choice:
        for i in business:
            if business_choice == i.first_class:
                product_list = Product.objects.filter(**business_search_dict)
                num = len(product_list)
            else:
                num = 0
            business_list.append(i.meaning)
            business_list1.append(i.meaning.strip('业务大类'))
            business_product.update({i.meaning: num})
            business_product1.append({"name": i.meaning, "value": num})
            # business_product_list.append([i.meaning, product_list])
    else:
        for i in business:
            business_search_dict.update({"business__first_class": i.first_class})
            product_list = Product.objects.filter(**business_search_dict)
            num = len(product_list)
            business_list.append(i.meaning)
            business_list1.append(i.meaning.strip('业务大类'))
            business_product.update({i.meaning: num})
            business_product1.append({"name": i.meaning, "value": num})
            business_product_list.append([i.meaning, product_list])

    # 技术形态
    if technology_choice:
        for i in technology:
            if technology_choice == i.first_class:
                product_list = Product.objects.filter(**technology_search_dict)
                num = len(product_list)
            else:
                num = 0
            technology_list.append(i.meaning)
            technology_product.update({i.meaning: num})
            technology_product1.append({"name": i.meaning, "value": num})
    else:
        for i in technology:
            technology_search_dict.update({"technology__first_class": i.first_class})
            product_list = Product.objects.filter(**technology_search_dict)
            technology_list.append(i.meaning)
            num = len(product_list)
            technology_product.update({i.meaning: num})
            technology_product1.append({"name": i.meaning, "value": num})

    # 成熟度-自主度
    maturity_independence = []
    num1 = 0
    num2 = 0
    maturity_independence_max_num=0
    if independence_choice:
        for ind in independence:
            if independence_choice == ind.first_class:
                if maturity_choice:
                    for mat in maturity:
                        if maturity_choice == mat.first_class:
                            maturity_independence_product_list = Product.objects.filter(**maturity_independence_search_dict)
                            num3 = len(maturity_independence_product_list)
                            maturity_independence_max_num=max(maturity_independence_max_num,num3)
                        else:
                            num3 = 0
                        maturity_independence_one = [num1, num2, num3]
                        maturity_independence.append(maturity_independence_one)
                        num2 += 1
                else:
                    for mat in maturity:
                        maturity_independence_search_dict["maturity__first_class"] = mat.first_class
                        maturity_independence_product_list = Product.objects.filter(**maturity_independence_search_dict)
                        num3 = len(maturity_independence_product_list)
                        maturity_independence_max_num = max(maturity_independence_max_num, num3)
                        maturity_independence_one = [num1, num2, num3]
                        maturity_independence.append(maturity_independence_one)
                        num2 += 1
            else:
                for mat in maturity:
                    num3 = 0
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            num1 += 1
            num2 = 0
    else:
        for ind in independence:
            maturity_independence_search_dict["independence__first_class"] = ind.first_class
            if maturity_choice:
                for mat in maturity:
                    if maturity_choice == mat.first_class:
                        maturity_independence_product_list = Product.objects.filter(**maturity_independence_search_dict)
                        num3 = len(maturity_independence_product_list)
                        maturity_independence_max_num = max(maturity_independence_max_num, num3)
                    else:
                        num3 = 0
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            else:
                for mat in maturity:
                    maturity_independence_search_dict["maturity__first_class"] = mat.first_class
                    maturity_independence_product_list = Product.objects.filter(**maturity_independence_search_dict)
                    num3 = len(maturity_independence_product_list)
                    maturity_independence_max_num = max(maturity_independence_max_num, num3)
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            num1 += 1
            num2 = 0

    # 业务领域-技术形态
    business_technology = []
    num1 = 0
    num2 = 0
    business_technology_max_num=0
    if technology_choice:
        for tec in technology:
            if technology_choice == tec.first_class:
                if business_choice:
                    for bus in business:
                        if business_choice == bus.first_class:
                            business_technology_product_list = Product.objects.filter(**business_technology_search_dict)
                            num3 = len(business_technology_product_list)
                            business_technology_max_num=max(business_technology_max_num,num3)
                        else:
                            num3 = 0
                        business_technology_one = [num1, num2, num3]
                        business_technology.append(business_technology_one)
                        num2 += 1
                else:
                    for bus in business:
                        business_technology_search_dict["business__first_class"] = bus.first_class
                        business_technology_product_list = Product.objects.filter(**business_technology_search_dict)
                        num3 = len(business_technology_product_list)
                        business_technology_max_num = max(business_technology_max_num, num3)
                        business_technology_one = [num1, num2, num3]
                        business_technology.append(business_technology_one)
                        num2 += 1
            else:
                for bus in business:
                    num3 = 0
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            num1 += 1
            num2 = 0
    else:
        for tec in technology:
            business_technology_search_dict["technology__first_class"] = tec.first_class
            if business_choice:
                for bus in business:
                    if business_choice == bus.first_class:
                        business_technology_product_list = Product.objects.filter(**business_technology_search_dict)
                        num3 = len(business_technology_product_list)
                        business_technology_max_num = max(business_technology_max_num, num3)
                    else:
                        num3 = 0
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            else:
                for bus in business:
                    business_technology_search_dict["business__first_class"] = bus.first_class
                    business_technology_product_list = Product.objects.filter(**business_technology_search_dict)
                    num3 = len(business_technology_product_list)
                    business_technology_max_num = max(business_technology_max_num, num3)
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            num1 += 1
            num2 = 0

    # 前端返回值
    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology,
                      "maturity_list": maturity_list, "independence_list": independence_list,
                      "business_list": business_list, "technology_list": technology_list,
                      "maturity_list1": maturity_list1, "independence_list1": independence_list1,
                      "business_list1": business_list1,
                      "maturity_product1": maturity_product1,
                      "independence_product1": independence_product1,
                      "business_product1": business_product1,
                      "technology_product1": technology_product1,
                      "maturity_independence": maturity_independence,
                      "business_technology": business_technology,
                      "maturity_independence_max_num": maturity_independence_max_num,
                      "business_technology_max_num": business_technology_max_num,
                      "check_box_list": check_box_list, "maturity_choice": maturity_choice,
                      "independence_choice": independence_choice, "business_choice": business_choice,
                      "technology_choice": technology_choice
                      })
    return render(request, template_name, page_dict)


# 产品详情页
def detail(request, template_name, bid):
    page_dict={}
    try:
        product = Product.objects.get(id=bid)
    except:
        raise Http404("产品不存在！")
    info = product.pack_data()
    page_dict.update({"info": info})
    product_file = product.save_name
    download_path_file = os.path.join(product_file)
    page_dict.update({"download_path_file": download_path_file})

    return render(request, template_name, page_dict)


# 属性化分类表
def table(request, template_name):
    page_dict = {}
    fil1 = {"attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('first_class','second_class')
    fil2 = {"attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('first_class','second_class')
    fil3 = {"attribute": 'B'}
    business = Attribute.objects.filter(**fil3).order_by('first_class','second_class')
    fil4 = {"attribute": 'T'}
    technology = Attribute.objects.filter(**fil4).order_by('first_class','second_class')

    page_dict.update({"maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
    return render(request, template_name, page_dict)