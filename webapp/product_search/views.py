# coding=utf-8
import re
import json

from cfsys.settings import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from webapp.models import *
from webapp.utils.query import get_query, create_data


def index(request, template_name):
    """
    查询 页面
    """
    page_dict = {}
    pCompany = COMPANY_CHOICE
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('first_class')
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('first_class')
    fil3 = {"ACT": 'c', "attribute": 'B'}
    business = Attribute.objects.filter(**fil3).order_by('first_class')
    fil4 = {"ACT": 'c', "attribute": 'T'}
    technology = Attribute.objects.filter(**fil4).order_by('first_class')

    page_dict.update({"pCompany": pCompany, "maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
    return render(request, template_name, page_dict)


def jump(request, template_name):
    return render(request, template_name)


@csrf_exempt
# 查询页数据
def search(request):
    fil = {"status": ProductStatus.PASS, "is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 展示页-查询展示
def show(request, template_name):
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

    # 属性大类查询
    fil1 = {"ACT": 'c', "attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('-first_class')
    maturity1 = Attribute.objects.filter(**fil1).order_by('first_class')
    fil2 = {"ACT": 'c', "attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('-first_class')
    independence1 = Attribute.objects.filter(**fil2).order_by('first_class')
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
    maturity_list2 = []
    independence_list2 = []
    #echarts 提示框所需产品数据
    maturity_product = []
    independence_product = []
    business_product = []
    technology_product = []
    maturity_independence_product = []
    business_technology_product = []
    #echarts绘图所需数据
    maturity_product1 = []
    independence_product1 = []
    business_product1 = []
    technology_product1 = []
    maturity_independence = []
    business_technology = []
    #echarts产品列表
    maturity_product_list = []
    independence_product_list = []
    business_product_list = []
    technology_product_list = []
    maturity_independence_product_list = []
    business_technology_product_list = []


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
        for i in maturity1:
            str = ""
            bpl = []
            if maturity_choice == i.first_class:
                product_list = Product.objects.filter(**maturity_search_dict)
                num = len(product_list)
                for s in product_list:
                    str = str + '<br/>' + s.product_name
                for s in product_list:
                    bpl.append(s.pack_data())
            else:
                num = 0
            maturity_list.append(i.meaning)
            name_m = re.findall(p1, i.meaning)
            if (name_m):
                maturity_list1.append(name_m[0])
            else:
                maturity_list1.append(i.meaning)
            maturity_product.append([str])
            maturity_product_list.append(bpl)
            maturity_product1.append({"name": i.meaning, "value": num})
    else:
        for i in maturity1:
            maturity_search_dict.update({"maturity__first_class": i.first_class})
            product_list = Product.objects.filter(**maturity_search_dict)
            num = len(product_list)
            str = ""
            bpl = []
            for s in product_list:
                str = str + '<br/>' + s.product_name
            for s in product_list:
                bpl.append(s.pack_data())
            maturity_list.append(i.meaning)
            name_m = re.findall(p1, i.meaning)
            if (name_m):
                maturity_list1.append(name_m[0])
            else:
                maturity_list1.append(i.meaning)
            maturity_product.append([str])
            maturity_product_list.append(bpl)
            maturity_product1.append({"name": i.meaning, "value": num})
            # print(maturity_search_dict)
    maturity_list2=maturity_list1.reverse()

    # 自主度
    if independence_choice:
        for i in independence1:
            str = ""
            bpl = []
            if independence_choice == i.first_class:
                product_list = Product.objects.filter(**independence_search_dict)
                num = len(product_list)
                for s in product_list:
                    str = str + '<br/>' + s.product_name
                for s in product_list:
                    bpl.append(s.pack_data())
            else:
                num = 0
            independence_list.append(i.meaning)
            name_i = re.findall(p1, i.meaning)
            if (name_i):
                independence_list1.append(name_i[0])
            else:
                independence_list1.append(i.meaning)
            independence_product.append([str])
            independence_product_list.append(bpl)
            independence_product1.append({"name": i.meaning, "value": num})
    else:
        for i in independence1:
            independence_search_dict.update({"independence__first_class": i.first_class})
            product_list = Product.objects.filter(**independence_search_dict)
            num = len(product_list)
            str = ""
            bpl = []
            for s in product_list:
                str = str + '<br/>' + s.product_name
            for s in product_list:
                bpl.append(s.pack_data())
            independence_list.append(i.meaning)
            name_i = re.findall(p1, i.meaning)
            if (name_i):
                independence_list1.append(name_i[0])
            else:
                independence_list1.append(i.meaning)
            independence_product.append([str])
            independence_product_list.append(bpl)
            independence_product1.append({"name": i.meaning, "value": num})
    independence_list2=independence_list1.reverse()

    # 业务领域
    if business_choice:
        for i in business:
            str = ""
            bpl = []
            if business_choice == i.first_class:
                product_list = Product.objects.filter(**business_search_dict)
                num = len(product_list)
                for s in product_list:
                    str = str + '<br/>' + s.product_name
                for s in product_list:
                    bpl.append(s.pack_data())
            else:
                num = 0
            business_list.append(i.meaning)
            business_list1.append(i.meaning.strip('业务大类'))
            business_product.append([str])
            business_product_list.append(bpl)
            business_product1.append({"name": i.meaning, "value": num})
    else:
        for i in business:
            business_search_dict.update({"business__first_class": i.first_class})
            product_list = Product.objects.filter(**business_search_dict)
            num = len(product_list)
            str = ""
            bpl = []
            for s in product_list:
                str = str + '<br/>' + s.product_name
            for s in product_list:
                bpl.append(s.pack_data())
            business_list.append(i.meaning)
            business_list1.append(i.meaning.strip('业务大类'))
            business_product.append([str])
            business_product_list.append(bpl)
            business_product1.append({"name": i.meaning, "value": num})

    # 技术形态
    if technology_choice:
        for i in technology:
            str = ""
            bpl = []
            if technology_choice == i.first_class:
                product_list = Product.objects.filter(**technology_search_dict)
                num = len(product_list)
                for s in product_list:
                    str = str + '<br/>' + s.product_name
                for s in product_list:
                    bpl.append(s.pack_data())
            else:
                num = 0
            technology_list.append(i.meaning)
            technology_product.append([str])
            technology_product_list.append(bpl)
            technology_product1.append({"name": i.meaning, "value": num})
    else:
        for i in technology:
            technology_search_dict.update({"technology__first_class": i.first_class})
            product_list = Product.objects.filter(**technology_search_dict)
            technology_list.append(i.meaning)
            num = len(product_list)
            str = ""
            bpl = []
            for s in product_list:
                str = str + '<br/>' + s.product_name
            for s in product_list:
                bpl.append(s.pack_data())
            technology_product.append([str])
            technology_product_list.append(bpl)
            technology_product1.append({"name": i.meaning, "value": num})


    # 成熟度-自主度
    num1 = 0
    num2 = 0
    maturity_independence_max_num = 0
    if independence_choice:
        for ind in independence:
            maturity_independence_product1 = []
            maturity_independence_product_list1=[]
            if independence_choice == ind.first_class:
                if maturity_choice:
                    for mat in maturity:
                        str = ""
                        bpl = []
                        if maturity_choice == mat.first_class:
                            product_list = Product.objects.filter(
                                **maturity_independence_search_dict)
                            num3 = len(product_list)
                            for s in product_list:
                                str = str + '<br/>' + s.product_name
                            for s in product_list:
                                bpl.append(s.pack_data())
                            maturity_independence_max_num = max(maturity_independence_max_num, num3)
                        else:
                            num3 = 0
                        maturity_independence_product1.append([str])
                        maturity_independence_product_list1.append(bpl)
                        maturity_independence_one = [num1, num2, num3]
                        maturity_independence.append(maturity_independence_one)
                        num2 += 1
                else:
                    for mat in maturity:
                        str = ""
                        bpl = []
                        maturity_independence_search_dict["maturity__first_class"] = mat.first_class
                        product_list = Product.objects.filter(**maturity_independence_search_dict)
                        num3 = len(product_list)
                        for s in product_list:
                            str = str + '<br/>' + s.product_name
                        for s in product_list:
                            bpl.append(s.pack_data())
                        maturity_independence_max_num = max(maturity_independence_max_num, num3)
                        maturity_independence_product1.append([str])
                        maturity_independence_product_list1.append(bpl)
                        maturity_independence_one = [num1, num2, num3]
                        maturity_independence.append(maturity_independence_one)
                        num2 += 1
            else:
                for mat in maturity:
                    num3 = 0
                    str = ""
                    bpl = []
                    maturity_independence_product1.append([str])
                    maturity_independence_product_list1.append(bpl)
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            maturity_independence_product.append(maturity_independence_product1)
            maturity_independence_product_list.append(maturity_independence_product_list1)
            num1 += 1
            num2 = 0
    else:
        for ind in independence:
            maturity_independence_product1 = []
            maturity_independence_product_list1 = []
            maturity_independence_search_dict["independence__first_class"] = ind.first_class
            if maturity_choice:
                for mat in maturity:
                    str = ""
                    bpl = []
                    if maturity_choice == mat.first_class:
                        product_list = Product.objects.filter(**maturity_independence_search_dict)
                        num3 = len(product_list)
                        for s in product_list:
                            str = str + '<br/>' + s.product_name
                        for s in product_list:
                            bpl.append(s.pack_data())
                        maturity_independence_max_num = max(maturity_independence_max_num, num3)
                    else:
                        num3 = 0
                    maturity_independence_product1.append([str])
                    maturity_independence_product_list1.append(bpl)
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            else:
                for mat in maturity:
                    maturity_independence_search_dict["maturity__first_class"] = mat.first_class
                    product_list = Product.objects.filter(**maturity_independence_search_dict)
                    num3 = len(product_list)
                    str = ""
                    bpl = []
                    for s in product_list:
                        str = str + '<br/>' + s.product_name
                    for s in product_list:
                        bpl.append(s.pack_data())
                    maturity_independence_max_num = max(maturity_independence_max_num, num3)
                    maturity_independence_product1.append([str])
                    maturity_independence_product_list1.append(bpl)
                    maturity_independence_one = [num1, num2, num3]
                    maturity_independence.append(maturity_independence_one)
                    num2 += 1
            maturity_independence_product.append(maturity_independence_product1)
            maturity_independence_product_list.append(maturity_independence_product_list1)
            num1 += 1
            num2 = 0

    # 业务领域-技术形态
    num1 = 0
    num2 = 0
    business_technology_max_num = 0
    if technology_choice:
        for tec in technology:
            business_technology_product1 = []
            business_technology_product_list1=[]
            if technology_choice == tec.first_class:
                if business_choice:
                    for bus in business:
                        str = ""
                        bpl = []
                        if business_choice == bus.first_class:
                            product_list = Product.objects.filter(**business_technology_search_dict)
                            num3 = len(product_list)
                            for s in product_list:
                                str = str + '<br/>' + s.product_name
                            for s in product_list:
                                bpl.append(s.pack_data())
                            business_technology_max_num = max(business_technology_max_num, num3)
                        else:
                            num3 = 0
                        business_technology_product1.append([str])
                        business_technology_product_list1.append(bpl)
                        business_technology_one = [num1, num2, num3]
                        business_technology.append(business_technology_one)
                        num2 += 1
                else:
                    for bus in business:
                        business_technology_search_dict["business__first_class"] = bus.first_class
                        product_list = Product.objects.filter(**business_technology_search_dict)
                        num3 = len(product_list)
                        str = ""
                        bpl = []
                        for s in product_list:
                            str = str + '<br/>' + s.product_name
                        for s in product_list:
                            bpl.append(s.pack_data())
                        business_technology_max_num = max(business_technology_max_num, num3)
                        business_technology_product1.append([str])
                        business_technology_product_list1.append(bpl)
                        business_technology_one = [num1, num2, num3]
                        business_technology.append(business_technology_one)
                        num2 += 1
            else:
                for bus in business:
                    num3 = 0
                    str = ""
                    bpl = []
                    business_technology_product1.append([str])
                    business_technology_product_list1.append(bpl)
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            business_technology_product.append(business_technology_product1)
            business_technology_product_list.append(business_technology_product_list1)
            num1 += 1
            num2 = 0
    else:
        for tec in technology:
            business_technology_product1 = []
            business_technology_product_list1 = []
            business_technology_search_dict["technology__first_class"] = tec.first_class
            if business_choice:
                for bus in business:
                    str = ""
                    bpl = []
                    if business_choice == bus.first_class:
                        product_list = Product.objects.filter(**business_technology_search_dict)
                        num3 = len(product_list)
                        for s in product_list:
                            str = str + '<br/>' + s.product_name
                        for s in product_list:
                            bpl.append(s.pack_data())
                        business_technology_max_num = max(business_technology_max_num, num3)
                    else:
                        num3 = 0
                    business_technology_product1.append([str])
                    business_technology_product_list1.append(bpl)
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            else:
                for bus in business:
                    business_technology_search_dict["business__first_class"] = bus.first_class
                    product_list = Product.objects.filter(**business_technology_search_dict)
                    num3 = len(product_list)
                    str = ""
                    bpl = []
                    for s in product_list:
                        str = str + '<br/>' + s.product_name
                    for s in product_list:
                        bpl.append(s.pack_data())
                    business_technology_max_num = max(business_technology_max_num, num3)
                    business_technology_product1.append([str])
                    business_technology_product_list1.append(bpl)
                    business_technology_one = [num1, num2, num3]
                    business_technology.append(business_technology_one)
                    num2 += 1
            business_technology_product.append(business_technology_product1)
            business_technology_product_list.append(business_technology_product_list1)
            num1 += 1
            num2 = 0
    # print(type(maturity_choice))
    # 前端返回值
    page_dict.update({"pCompany": pCompany,
                      "maturity": maturity,
                      "independence": independence,
                      "business": business, "technology": technology,
                      "maturity1": maturity1,
                      "independence1": independence1,

                      "maturity_list": maturity_list, "independence_list": independence_list,
                      "business_list": business_list, "technology_list": technology_list,
                      "maturity_list1": maturity_list1, "independence_list1": independence_list1,
                      "business_list1": business_list1,
                      "maturity_list2": maturity_list2, "independence_list2": independence_list2,

                      "maturity_product1": maturity_product1,
                      "independence_product1": independence_product1,
                      "business_product1": business_product1,
                      "technology_product1": technology_product1,
                      "maturity_independence": maturity_independence,
                      "business_technology": business_technology,

                      "maturity_product": maturity_product,
                      "independence_product": independence_product,
                      "business_product": business_product,
                      "technology_product": technology_product,
                      "maturity_independence_product": maturity_independence_product,
                      "business_technology_product": business_technology_product,

                      "maturity_product_list": json.dumps(maturity_product_list),
                      "independence_product_list": json.dumps(independence_product_list),
                      "business_product_list": json.dumps(business_product_list),
                      "technology_product_list": json.dumps(technology_product_list),
                      "maturity_independence_product_list": maturity_independence_product_list,
                      "business_technology_product_list": business_technology_product_list,

                      "maturity_independence_max_num": maturity_independence_max_num,
                      "business_technology_max_num": business_technology_max_num,

                      # "check_box_list": check_box_list,
                      "maturity_choice": maturity_choice,
                      "independence_choice": independence_choice, "business_choice": business_choice,
                      "technology_choice": technology_choice,

                      "check_box_list": json.dumps(check_box_list),
                      # "maturity_choice": json.dumps(maturity_choice),
                      # "independence_choice": json.dumps(independence_choice),
                      # "business_choice": json.dumps(business_choice),
                      # "technology_choice": json.dumps(technology_choice),
                      })
    # print(page_dict)
    return render(request, template_name, page_dict)


# 图表产品列表
def chart_list(request, template_name):
    # print(json.loads(request.POST.get("check_box_list")))
    res = {
        "product_list":json.loads(request.POST.get("product_list")),
        "check_box_list ": json.loads(request.POST.get("check_box_list")),
        "maturity_choice ": request.POST.get("maturity_choice"),
        "independence_choice ": request.POST.get("independence_choice"),
        "business_choice ": request.POST.get("business_choice"),
        "technology_choice ": request.POST.get("technology_choice")
    }
    # print(type(request.POST.get("maturity_choice")))
    return render(request, template_name, res)


# # 图表产品列表返回展示查询结果
# def list_return(request):
#
#     return HttpResponseRedirect("/product_search/page_show_product/search/")

# 产品详情页
def detail(request, template_name, bid):
    page_dict = {}
    try:
        product = Product.objects.get(id=bid)
    except:
        raise Http404("产品不存在！")
    info = product.pack_data()
    page_dict.update({"info": info})
    product_file = ''
    if product.save_name:
        product_file = product.save_name
    download_path_file = os.path.join(product_file)
    page_dict.update({"download_path_file": download_path_file})

    return render(request, template_name, page_dict)


# 属性化分类表
def table(request, template_name):
    page_dict = {}
    fil1 = {"attribute": 'M'}
    maturity = Attribute.objects.filter(**fil1).order_by('first_class', 'second_class')
    fil2 = {"attribute": 'I'}
    independence = Attribute.objects.filter(**fil2).order_by('first_class', 'second_class')
    fil3 = {"attribute": 'B'}
    business = Attribute.objects.filter(**fil3).order_by('first_class', 'second_class')
    fil4 = {"attribute": 'T'}
    technology = Attribute.objects.filter(**fil4).order_by('first_class', 'second_class')
    # print(maturity)
    page_dict.update({"maturity": maturity,
                      "independence": independence, "business": business, "technology": technology})
    return render(request, template_name, page_dict)
