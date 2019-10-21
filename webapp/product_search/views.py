# coding=utf-8
import os
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
    fil = {"is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


@csrf_exempt
# 展示页面数据
def show(request, template_name):
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
    maturity_list = []
    independence_list = []
    business_list = []
    technology_list = []
    maturity_product = {}
    independence_product = {}
    business_product_list = []
    business_product = {}
    business_product1 = []
    technology_product = {}
    for i in maturity:
        product_list = Product.objects.filter(maturity__first_class=i.first_class)
        num = len(product_list)
        maturity_list.append(i.meaning)
        maturity_product.update({i.meaning: num})
    # print(maturity_list)
    for i in independence:
        product_list = Product.objects.filter(independence__first_class=i.first_class)
        num = len(product_list)
        independence_list.append(i.meaning)
        independence_product.update({i.meaning: num})
    for i in business:
        product_list = Product.objects.filter(business__first_class=i.first_class)
        num = len(product_list)
        business_list.append(i.meaning)
        # business_product_listandnum = {product_list: num}
        business_product.update({i.meaning: num})
        business_product1.append({"name": i.meaning, "value": num})
        business_product_list.append([i.meaning, product_list])
        # print(business_product)
        # business_product_list.update({i:product_list})
        # for i in business:
        #     product_list = Product.objects.filter(business__first_class=i.first_class)
        #     num = len(product_list)
        #     business_product_listandnum.update({product_list:num})
        #     business_product.update({i: business_product_listandnum})
    # print(business_product_list)
    # print(business_product1)

    for i in technology:
        product_list = Product.objects.filter(technology__first_class=i.first_class)
        technology_list.append(i.meaning)
        num = len(product_list)
        technology_product.update({i.meaning: num})

    maturity_independence = []
    business_technology = []
    num1 = 0
    num2 = 0
    for mat in maturity:
        for ind in independence:
            maturity_independence_fil1 = {"maturity__first_class": mat.first_class,
                                          "independence__first_class": ind.first_class}
            maturity_independence_product_list = Product.objects.filter(**maturity_independence_fil1)
            num3 = len(maturity_independence_product_list)
            maturity_independence_one = [num1, num2, num3]
            num2 += 1
            maturity_independence.append(maturity_independence_one)
        num1 += 1
        num2 = 0

    num4 = 0
    num5 = 0
    for bus in business:
        for tec in technology:
            business_technology_fil1 = {"business__first_class": bus.first_class,
                                        "technology__first_class": tec.first_class}
            business_technology_product_list = Product.objects.filter(**business_technology_fil1)
            num6 = len(business_technology_product_list)
            business_technology_one = [num4, num5, num6]
            num5 += 1
            business_technology.append(business_technology_one)
        num4 += 1
        num5 = 0

    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology,
                      "maturity_list": maturity_list, "independence_list": independence_list,
                      "business_list": business_list, "technology_list": technology_list,
                      "maturity_product": maturity_product,
                      "independence_product": independence_product,
                      "business_product": business_product,
                      "business_product1": business_product1,
                      "business_product_list": business_product_list,
                      "technology_product": technology_product,
                      "maturity_independence": maturity_independence})
    return render(request, template_name, page_dict)


@csrf_exempt
# 产品详情页
def detail(request, template_name, bid):
    try:
        product = Product.objects.get(id=bid)
    except:
        raise Http404("产品不存在！")
    info = product.pack_data()
    product_file = product.save_name
    download_path_file = os.path.join(product_file)
    return render(request, template_name, {"info": info, "download_path_file": download_path_file})
