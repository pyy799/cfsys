
import os
import re
import shutil
import time
import xlrd
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from webapp.shortcuts.decorator import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webapp.models import *
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *
from webapp.utils.query import get_query, create_data

@login_required
@permission_required('webapp.product_information_manege_check')
def index(request, template_name):
    return render(request, template_name)


# 单纯跳转页面
def jump(request, template_name):
    return render(request, template_name)

# 新建及更新页面
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def page_new_product(request, template_name):
    page_dict = {}
    company_choice = COMPANY_CHOICE
    apply_choice = APPLY_CHOICE
    fil = {"status": ProductStatus.WAIT_SUBMIT}
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list = Product.objects.filter(**fil)
    waitsubmit_num = product_list.count()
    fil = {"status": ProductStatus.FAIL}
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list = Product.objects.filter(**fil)
    nopass_num = product_list.count()
    page_dict.update({"company_choice": company_choice, "apply_choice": apply_choice, "waitsubmit_num":waitsubmit_num,
                      "nopass_num":nopass_num})

    return render(request, template_name, page_dict)

# 更新页面数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_data(request):
    fil = {"status": ProductStatus.PASS, "is_vaild": True}
    # 只能看到自己公司的
    user = request.user.userprofile
    group = Group.objects.get(user=user)
    if not group.id == 1:
        fil.update({"pCompany": user.uCompany})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 更新页面停用操作
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_invalid(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("停用失败!"+str(e))
    product.apply_type = ApplyStatus.INVALID
    product.status = ProductStatus.WAIT_SUBMIT
    product.save()
    return ajax_success()


# 更新页面删除操作
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_delete(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("取消失败!"+str(e))
    product.apply_type = ApplyStatus.DELETE
    product.status = ProductStatus.WAIT_SUBMIT
    product.save()
    return ajax_success()


# 新建及更新页面“待提交”页签数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def wait_submit(request):
    fil = {"status": ProductStatus.WAIT_SUBMIT}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 批量新建
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def new_many(request):
    user = request.user.userprofile
    group = Group.objects.get(user=user)
    now = int(time.time())
    product_list = []
    zip_file_name = ''
    excel_file_name = ''
    i = 0
    try:
        if request.method != "POST":
            return ajax_error("上传失败")
        zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
        save_zip = os.path.splitext(zip.name)[1]
        if save_zip != '.zip' and save_zip != '.rar':
            raise Exception("审批信息文件类型有误！")
        zip_file_name = save_name+save_zip
        if not os.path.exists(PRODUCT_TEMP_ZIP_PATH):
            os.makedirs(PRODUCT_TEMP_ZIP_PATH)
        destination = open(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name), "wb+")  # 把文件写入
        for chunk in zip.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        excel = request.FILES.get("excel", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_excel = os.path.splitext(excel.name)[1]
        if save_excel != '.xls' and save_excel != '.xlsx':
            raise Exception("产品信息文件类型有误！")
        excel_file_name = save_name+save_excel
        if not os.path.exists(PRODUCT_TEMP_EXCEL_PATH):
            os.makedirs(PRODUCT_TEMP_EXCEL_PATH)
        destination = open(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name), "wb+")  # 把文件写入
        for chunk in excel.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        file = os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name)
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_index(0)
        nrows = sheet.nrows

        for i in range(1, nrows):
            row = sheet.row_values(i)
            product_name = str(row[0]).strip()
            if not product_name:
                raise Exception("产品名称不能为空！")
            if len(product_name)>64:
                raise Exception("产品名称不能超过64个字符！")
            product_exist = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID)& Q(status=ProductStatus.PASS)).filter(product_name=product_name)
            if len(product_exist)>0:
                raise Exception("产品名称已存在！")
            old_product_name = str(row[1]).strip()
            if len(old_product_name)>64:
                raise Exception("旧产品名称不能超过64个字符！")
            if old_product_name == 'N.A.' or not old_product_name:
                old_product_name = None
            introduction = str(row[2]).strip()
            if not introduction:
                raise Exception("产品描述不能为空！")
            if len(introduction)>1024:
                raise Exception("产品描述不能超过1024个字符！")
            is_overlap = str(row[3]).strip()
            if is_overlap:
                if is_overlap=="是":
                    is_overlap = True
                elif is_overlap=="否":
                    is_overlap = False
                else:
                    raise Exception("是否重叠填写有误！")
            target_field = str(row[4]).strip()
            if len(target_field)>1024:
                raise Exception("目标行业不能超过1024个字符！")
            apply_situation = str(row[5]).strip()
            if len(apply_situation)>1024:
                raise Exception("应用场景不能超过1024个字符！")
            example = str(row[6]).strip()
            if len(example)>1024:
                raise Exception("市场案例不能超过1024个字符！")
            one_year_money = str(row[7]).strip()
            if one_year_money:
                if len(one_year_money) > 11:
                    raise Exception("过去一年销售额不能超过11个字符！")
                if type(row[7]) is int or type(row[7]) is float:
                    one_year_money = float(row[7])
                else:
                    raise Exception("过去一年销售额填写有误！")
            else:
                one_year_money = 0
            one_year_num = str(row[8]).strip()
            if one_year_num:
                if len(one_year_num) > 11:
                    raise Exception("过去一年销售数量不能超过11个字符！")
                if re.findall(r"\d+", one_year_num):
                    one_year_num = int(re.findall(r"\d+", str(row[8]))[0])
                else:
                    raise Exception("过去一年销售数量填写有误！")
            else:
                one_year_num = 0
            three_year_money = str(row[9]).strip()
            if three_year_money:
                if len(three_year_money) > 11:
                    raise Exception("过去三年销售额不能超过11个字符！")
                if type(row[9]) is int or type(row[9]) is float:
                    three_year_money = float(row[9])
                else:
                    raise Exception("过去三年销售额填写有误！")
            else:
                three_year_money = 0
            three_year_num = str(row[10]).strip()
            if three_year_num:
                if len(three_year_num) > 11:
                    raise Exception("过去三年销售数量不能超过11个字符！")
                if re.findall(r"\d+", three_year_num):
                    three_year_num = int(re.findall(r"\d+", str(row[10]))[0])
                else:
                    raise Exception("过去三年销售数量填写有误！")
            else:
                three_year_num = 0
            pCompany = str(row[11]).strip()
            if pCompany:
                if pCompany in dict(COMPANY_CHOICE).values():
                    if group.id != 1:  # 不是超级管理员
                        if pCompany == dict(COMPANY_CHOICE).get(user.uCompany):
                            pCompany = user.uCompany
                        else:
                            raise Exception("公司只能为当前登陆者所在公司！")
                    else:
                        pCompany = get_key(dict(COMPANY_CHOICE), pCompany)
                else:
                    raise Exception("公司填写有误！")
            else:
                raise Exception("公司不能为空！")

            maturity = str(row[12]).strip()
            independence = str(row[13]).strip()
            business = str(row[14]).strip()
            technology = str(row[15]).strip()
            if maturity and independence and business and technology:
                maturity_a = Attribute.objects.filter(first_class=maturity)
                independence_a = Attribute.objects.filter(first_class=independence)
                business_a = Attribute.objects.filter(second_class=business)
                technology_a = Attribute.objects.filter(second_class=technology)
                if not maturity_a:
                    raise Exception("成熟度填写有误！")
                if not independence_a:
                    raise Exception("自主度填写有误！")
                if not business_a:
                    raise Exception("业务类别填写有误！")
                if not technology_a:
                    raise Exception("技术性态填写有误！")
            else:
                raise Exception("属性不能为空！")

            contact_people = str(row[16]).strip()
            if not contact_people:
                raise Exception("联系人不能为空！")
            if len(contact_people) > 64:
                raise Exception("联系人不能超过64个字符！")
            remark = str(row[17]).strip()
            if len(remark) > 1024:
                raise Exception("备注不能超过1024个字符！")
            upload_time = datetime.date.today()
            real_name = zip.name

            attribute_num = maturity+independence+business+technology
            status = ProductStatus.WAIT_SUBMIT
            apply_type = ApplyStatus.NEW
            version = 1
            is_vaild = False

            product = Product()
            product_list.append(product)
            product.save()
            product.product_num = product.id
            product.product_name = product_name
            product.old_product_name = old_product_name
            product.introduction = introduction
            product.is_overlap = is_overlap
            product.target_field = target_field
            product.apply_situation = apply_situation
            product.example = example
            product.one_year_money = one_year_money
            product.one_year_num = one_year_num
            product.three_year_money = three_year_money
            product.three_year_num = three_year_num
            product.pCompany = pCompany
            product.contact_people = contact_people
            product.remark = remark
            product.uploader = user
            product.upload_time = upload_time
            product.real_name = real_name
            product.save_name = zip_file_name
            product.maturity = maturity_a[0]
            product.independence = independence_a[0]
            product.business = business_a[0]
            product.technology = technology_a[0]
            product.attribute_num = attribute_num
            product.status = status
            product.apply_type = apply_type
            product.version = version
            product.is_vaild = is_vaild
            product.save()
    except Exception as e:
        if product_list:
            for product in product_list:
                product.delete()
        if zip_file_name:
            os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name))
        if excel_file_name:
            os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name))
        if i:
            return ajax_error("产品文件上传失败:"+"第"+str(i+1)+"行"+str(e))
        else:
            return ajax_error("产品文件上传失败:" + str(e))

    # '产品名称', '旧产品名称', '产品描述', '是否重叠', '目标行业', '应用场景', '市场案例', '过去一年销售额（万元）',
    # '过去一年销售数量（套/件/组）', '过去三年销售数量（万元）', '过去三年销售数量（套/件/组）', '公司', 'M\n（成熟度）',
    # 'I\n（自主度）', 'B\n（业务类别）', 'T\n（技术形态）', '联系人及联系方式', '备注'

    return ajax_success()


# 批量更新
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_many(request):
    user = request.user.userprofile
    group = Group.objects.get(user=user)
    now = int(time.time())
    product_list = []
    zip_file_name = ''
    excel_file_name = ''
    i = 0
    product_invaild_list = []
    try:
        if request.method != "POST":
            return ajax_error("上传失败")
        zip = request.FILES.get("update_zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
        save_zip = os.path.splitext(zip.name)[1]
        if save_zip != '.zip' and save_zip != '.rar':
            raise Exception("审批信息文件类型有误！")
        zip_file_name = save_name+save_zip
        if not os.path.exists(PRODUCT_TEMP_ZIP_PATH):
            os.makedirs(PRODUCT_TEMP_ZIP_PATH)
        destination = open(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name), "wb+")  # 把文件写入
        for chunk in zip.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        excel = request.FILES.get("update_excel", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_excel = os.path.splitext(excel.name)[1]
        if save_excel != '.xls' and save_excel != '.xlsx':
            raise Exception("产品信息文件类型有误！")
        excel_file_name = save_name+save_excel
        if not os.path.exists(PRODUCT_TEMP_EXCEL_PATH):
            os.makedirs(PRODUCT_TEMP_EXCEL_PATH)
        destination = open(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name), "wb+")  # 把文件写入
        for chunk in excel.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        file = os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name)
        wb = xlrd.open_workbook(file)
        sheet = wb.sheet_by_index(0)
        nrows = sheet.nrows
        for i in range(1, nrows):
            product_exist = None
            row = sheet.row_values(i)
            product_name = str(row[0]).strip()
            if not product_name:
                raise Exception("产品名称不能为空！")

            if len(product_name)>64:
                raise Exception("产品名称不能超过64个字符！")
            old_product_name = str(row[1]).strip()
            if len(old_product_name)>64:
                raise Exception("旧产品名称不能超过64个字符！")
            if old_product_name == 'N.A.' or not old_product_name:
                old_product_name = None
            introduction = str(row[2]).strip()
            if not introduction:
                raise Exception("产品描述不能为空！")
            if len(introduction)>1024:
                raise Exception("产品描述不能超过1024个字符！")
            is_overlap = str(row[3]).strip()
            if is_overlap:
                if is_overlap=="是":
                    is_overlap = True
                elif is_overlap=="否":
                    is_overlap = False
                else:
                    raise Exception("是否重叠填写有误！")
            target_field = str(row[4]).strip()
            if len(target_field) > 1024:
                raise Exception("目标行业不能超过1024个字符！")
            apply_situation = str(row[5]).strip()
            if len(apply_situation) > 1024:
                raise Exception("应用场景不能超过1024个字符！")
            example = str(row[6]).strip()
            if len(example) > 1024:
                raise Exception("市场案例不能超过1024个字符！")
            one_year_money = str(row[7]).strip()
            if one_year_money:
                if len(one_year_money) > 11:
                    raise Exception("过去一年销售额不能超过11个字符！")
                if type(row[7]) is int or type(row[7]) is float:
                    one_year_money = float(row[7])
                else:
                    raise Exception("过去一年销售额填写有误！")
            else:
                one_year_money = 0
            one_year_num = str(row[8]).strip()
            if one_year_num:
                if len(one_year_num) > 11:
                    raise Exception("过去一年销售数量不能超过11个字符！")
                if re.findall(r"\d+", one_year_num):
                    one_year_num = int(re.findall(r"\d+", str(row[8]))[0])
                else:
                    raise Exception("过去一年销售数量填写有误！")
            else:
                one_year_num = 0
            three_year_money = str(row[9]).strip()
            if three_year_money:
                if len(three_year_money) > 11:
                    raise Exception("过去三年销售额不能超过11个字符！")
                if type(row[9]) is int or type(row[9]) is float:
                    three_year_money = float(row[9])
                else:
                    raise Exception("过去三年销售额填写有误！")
            else:
                three_year_money = 0
            three_year_num = str(row[10]).strip()
            if three_year_num:
                if len(three_year_num) > 11:
                    raise Exception("过去三年销售数量不能超过11个字符！")
                if re.findall(r"\d+", three_year_num):
                    three_year_num = int(re.findall(r"\d+", str(row[10]))[0])
                else:
                    raise Exception("过去三年销售数量填写有误！")
            else:
                three_year_num = 0

            pCompany = str(row[11]).strip()
            if pCompany:
                if pCompany in dict(COMPANY_CHOICE).values():
                    if group.id != 1:  # 不是超级管理员
                        if pCompany == dict(COMPANY_CHOICE).get(user.uCompany):
                            pCompany = user.uCompany
                        else:
                            raise Exception("公司只能为当前登陆者所在公司！")
                    else:
                        pCompany = get_key(dict(COMPANY_CHOICE), pCompany)
                else:
                    raise Exception("公司填写有误！")
            else:
                raise Exception("公司不能为空！")

            maturity = str(row[12]).strip()
            independence = str(row[13]).strip()
            business = str(row[14]).strip()
            technology = str(row[15]).strip()
            if maturity and independence and business and technology:
                maturity_a = Attribute.objects.filter(first_class=maturity)
                independence_a = Attribute.objects.filter(first_class=independence)
                business_a = Attribute.objects.filter(second_class=business)
                technology_a = Attribute.objects.filter(second_class=technology)
                if not maturity_a:
                    raise Exception("成熟度填写有误！")
                if not independence_a:
                    raise Exception("自主度填写有误！")
                if not business_a:
                    raise Exception("业务类别填写有误！")
                if not technology_a:
                    raise Exception("技术性态填写有误！")
            else:
                raise Exception("属性不能为空！")

            contact_people = str(row[16]).strip()
            if not contact_people:
                raise Exception("联系人不能为空！")
            if len(contact_people) > 64:
                raise Exception("联系人不能超过64个字符！")
            remark = str(row[17]).strip()
            if len(remark) > 1024:
                raise Exception("备注不能超过1024个字符！")

            # 判断是否是更新
            product_exist_list = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID)& Q(status=ProductStatus.PASS))\
                .filter(product_name=product_name)  # 在所有没停用的产品里找重名的
            if len(product_exist_list)>0: # 有重名的，看重名是否合法
                if group.id == 1: # 超级管理员
                    b = product_exist_list.filter(Q(status=ProductStatus.PASS) & Q(is_vaild=True)).order_by('-version')
                else: # 分公司
                    b = product_exist_list.filter(Q(pCompany=user.uCompany) & Q(status=ProductStatus.PASS) & Q(is_vaild=True))\
                        .order_by('-version')
                # b是合法重名的
                if len(product_exist_list) > len(b): # 有不合法重名产品
                    raise Exception("产品名称重复！")
                else: # 重名合法->是更新
                    product_exist = b[0]
            else: # 产品名称没和自己公司的重复->查旧产品名称
                if old_product_name:
                    if group.id == 1:  # 超级管理员
                        old_product_exist_list = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID) & Q(status=ProductStatus.PASS))\
                            .filter(Q(product_name=old_product_name) & Q(status=ProductStatus.PASS) & Q(is_vaild=True))\
                            .order_by('-version')
                    else:
                        old_product_exist_list = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID) & Q(status=ProductStatus.PASS))\
                            .filter(Q(product_name=old_product_name) & Q(pCompany=user.uCompany) & Q(status=ProductStatus.PASS) & Q(is_vaild=True)). \
                            order_by('-version')
                    if len(old_product_exist_list) > 0:  # 旧产品名称和自己公司合法产品的重复->是更新
                        product_exist = old_product_exist_list[0]
                    else:
                        product_exist = None
                else:  # 没有旧产品名称->是新建
                    product_exist = None

            if product_exist: # 更新的话
                # 更新内容和原来判重
                if  product_name==product_exist.product_name and old_product_name==product_exist.old_product_name and \
                    introduction==product_exist.introduction and is_overlap==product_exist.is_overlap and\
                    target_field==product_exist.target_field and apply_situation==product_exist.apply_situation and \
                    example == product_exist.example and one_year_money==product_exist.one_year_money and \
                    one_year_num == product_exist.one_year_num and three_year_money==product_exist.three_year_money and\
                    three_year_num == product_exist.three_year_num and pCompany==product_exist.pCompany and \
                    Attribute.objects.get(first_class=maturity) == product_exist.maturity and \
                    Attribute.objects.get(first_class=independence) == product_exist.independence and \
                    Attribute.objects.get(second_class=business) == product_exist.business and \
                    Attribute.objects.get(second_class=technology) == product_exist.technology and \
                    contact_people==product_exist.contact_people and remark == product_exist.remark:
                    continue  # 都一样就跳过
                else: # 有不一样的，更新
                    apply_type = ApplyStatus.ALTER
                    version = product_exist.version+1
            else: # 新建
                apply_type = ApplyStatus.NEW
                version = 1

            upload_time = datetime.date.today()
            real_name = zip.name
            attribute_num = maturity+independence+business+technology
            status = ProductStatus.WAIT_SUBMIT
            is_vaild = False

            product = Product()
            product_list.append(product)
            product.save()
            if apply_type == ApplyStatus.NEW:
                product.product_num = product.id
            else:
                product.product_num = product_exist.product_num
            product.product_name = product_name
            product.old_product_name = old_product_name
            product.introduction = introduction
            product.is_overlap = is_overlap
            product.target_field = target_field
            product.apply_situation = apply_situation
            product.example = example
            product.one_year_money = one_year_money
            product.one_year_num = one_year_num
            product.three_year_money = three_year_money
            product.three_year_num = three_year_num
            product.pCompany = pCompany
            product.contact_people = contact_people
            product.remark = remark
            product.uploader = user
            product.upload_time = upload_time
            product.real_name = real_name
            product.save_name = zip_file_name
            product.maturity = maturity_a[0]
            product.independence = independence_a[0]
            product.business = business_a[0]
            product.technology = technology_a[0]
            product.attribute_num = attribute_num
            product.status = status
            product.apply_type = apply_type
            product.version = version
            product.is_vaild = is_vaild
            product.save()
            if product_exist:
                product_exist.is_vaild = False
                product_exist.save()
                product_invaild_list.append(product_exist)
    except Exception as e:
        if product_list:
            for product in product_list:
                product.delete()
        if product_invaild_list:
            for product in product_invaild_list:
                product_exist.is_vaild = True
                product_exist.save()
        if zip_file_name:
            os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name))
        if excel_file_name:
            os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name))
        if i:
            return ajax_error("产品文件上传失败:"+"第"+str(i+1)+"行"+str(e))
        else:
            return ajax_error("产品文件上传失败:" + str(e))

    # '产品名称', '旧产品名称', '产品描述', '是否重叠', '目标行业', '应用场景', '市场案例', '过去一年销售额（万元）',
    # '过去一年销售数量（套/件/组）', '过去三年销售数量（万元）', '过去三年销售数量（套/件/组）', '公司', 'M\n（成熟度）',
    # 'I\n（自主度）', 'B\n（业务类别）', 'T\n（技术形态）', '联系人及联系方式', '备注'

    return ajax_success()


# 新建/修改产品页面
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_product(request, pid, template_name):
    user = request.user.userprofile
    group = Group.objects.get(user=user)
    user_company = ''
    user_company_name = ''
    pid = int(pid)
    product_value = None
    file_name = []
    company_choice = COMPANY_CHOICE
    fil1 = {"ACT": 'c', "attribute": 'M'}
    m_choice = Attribute.objects.filter(**fil1)
    fil2 = {"ACT": 'c', "attribute": 'I'}
    i_choice = Attribute.objects.filter(**fil2)
    fil3 = {"ACT": 't', "attribute": 'B'}
    b_choice = Attribute.objects.filter(**fil3)
    fil4 = {"ACT": 't', "attribute": 'T'}
    t_choice = Attribute.objects.filter(**fil4)
    if pid != 0:
        try:
            product = Product.objects.get(id=pid)
            product_value = product.pack_data()
            real_name = product.real_name
            file_name = real_name
            print(real_name)
        except Exception as e:
            return ajax_error("产品不存在!"+str(e))
    else:  # 新建
        path = os.path.join(TEMP_FILES_PATH, user.username)   # 如果是新建，则原文件在temp/user路径
        if os.path.exists(path) and len(os.listdir(path)):
            file_name = os.listdir(path)[0].split('_')[0]
    if group.id != 1: # 不是超级管理员
        user_company = user.uCompany
        user_company_name = dict(COMPANY_CHOICE).get(user_company)

    page_dict = {"pid": pid, "product": product_value, "file_name": file_name, "company_choice": company_choice,
                 "m_choice": m_choice, "i_choice": i_choice, "b_choice":b_choice, "t_choice":t_choice,
                 "user_company":user_company, "user_company_name":user_company_name}
    return render(request, template_name, page_dict)


# 编辑产品页面上传文件
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_upload_file(request, pid):
    user = request.user.userprofile
    now = int(time.time())
    pid = int(pid)
    try:
        if pid != 0:  # 修改或更新
            product = Product.objects.get(id=pid)
            if request.method != "POST":
                raise Exception("审批文件上传失败!")
            zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
            save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
            save_zip = os.path.splitext(zip.name)[1]
            if save_zip != '.zip' and save_zip != '.rar':
                raise Exception("审批文件类型有误！")
            zip_file_name = save_name+save_zip
            path = PRODUCT_TEMP_ZIP_PATH
            if not os.path.exists(path):
                os.makedirs(path)
            destination = open(os.path.join(path, zip_file_name), "wb+")  # 把文件写入
            for chunk in zip.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
            product.save_name = zip_file_name
            product.real_name = zip.name
            product.save()
        else:  # 新建
            if request.method != "POST":
                raise Exception("审批文件上传失败!")
            zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
            save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
            save_zip = os.path.splitext(zip.name)[1]
            if save_zip != '.zip' and save_zip != '.rar':
                raise Exception("审批文件类型有误！")
            zip_file_name = save_name+save_zip
            path = os.path.join(TEMP_FILES_PATH, user.username)
            if not os.path.exists(path):
                os.makedirs(path)
            destination = open(os.path.join(path, zip_file_name), "wb+")  # 把文件写入
            for chunk in zip.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()
    except Exception as e:
        return ajax_error(str(e))
    return ajax_success()


# 编辑产品页面删除已上传文件
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_delete_file(request, pid):
    user = request.user.userprofile
    pid = int(pid)
    if pid != 0:
        try:
            product = Product.objects.get(id=pid)
            full_name = product.save_name
            status = product.status
            product_list = Product.objects.filter(save_name=full_name)
            if len(product_list)==1:  # 如果还有关联产品就不删
                if status == ProductStatus.WAIT_SUBMIT:
                    os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, full_name))
                else:
                    os.remove(os.path.join(PRODUCT_ZIP_PATH, full_name))
            product.save_name = None
            product.real_name = None
            product.save()
        except Exception as e:
            return ajax_error("找不到产品!"+str(e))
    else:  # 新建-编辑-删文件
        path = os.path.join(TEMP_FILES_PATH, user.username)
        if os.path.exists(path):
            shutil.rmtree(path)

    return HttpResponseRedirect("/product_management/edit_product/"+str(pid)+"/")


# 编辑产品页面提交
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_submit(request, pid):
    user = request.user.userprofile
    pid = int(pid)
    product_old = None
    product = None
    try:
        file_name = request.POST.get("file_name")
        if not file_name:
            raise Exception("未上传审批文件！")
        if file_name == '[]' or file_name == 'None':
            raise Exception("未上传审批文件！")
        product_name = request.POST.get("product_name").strip()
        if pid == 0:  # 新建
            flag_new = True
        else: # 单个更新或待提交修改或未通过修改
            product = Product.objects.get(id=pid)
            if product.apply_type == ApplyStatus.NEW:
                flag_new = True
            else:
                flag_new = False

        if flag_new:  # 新建
            product_exist = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID) & Q(status=ProductStatus.PASS))\
                .filter(product_name=product_name)
            count = len(product_exist)
            if count > 0:
                raise Exception("产品名称已存在!")
        else:  # 更新
            old_name = Product.objects.filter(product_num=product.product_num).order_by('-version')[0].product_name
            if product_name != old_name:
                product_exist = Product.objects.exclude(Q(apply_type=ApplyStatus.INVALID) & Q(status=ProductStatus.PASS)) \
                .filter(product_name=product_name)
                count = len(product_exist)
                if count > 0:
                    raise Exception("产品名称已存在!")

        old_product_name = request.POST.get("old_product_name")
        if old_product_name == 'N.A.' or not old_product_name:
            old_product_name = None
        else:
            old_product_name = old_product_name.strip()

        pCompany = request.POST.get("pCompany").strip()
        is_overlap = request.POST.get("is_overlap") or ''
        maturity = request.POST.get("maturity") or ''
        independence = request.POST.get("independence") or ''
        business = request.POST.get("business") or ''
        technology = request.POST.get("technology") or ''

        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        if request.POST.get("one_year_money"):
            if not str(request.POST.get("one_year_money")).strip():
                one_year_money = 0
            elif pattern.match(str(request.POST.get("one_year_money")).strip()):
                one_year_money= float(request.POST.get("one_year_money") or 0)
            else:
                raise Exception("过去一年销售额填写有误！")
        else:
            one_year_money = 0
        one_year_num= int(request.POST.get("one_year_num") or 0)
        if request.POST.get("three_year_money"):
            if not str(request.POST.get("three_year_money")).strip():
                three_year_money = 0
            elif pattern.match(str(request.POST.get("three_year_money")).strip()):
                three_year_money = float(request.POST.get("three_year_money") or 0)
            else:
                raise Exception("过去三年销售额填写有误！")
        else:
            three_year_money = 0
        three_year_num= int(request.POST.get("three_year_num") or 0)
        contact_people= request.POST.get("contact_people").strip()
        introduction= request.POST.get("introduction").strip()
        target_field = request.POST.get("target_field").strip()
        apply_situation = request.POST.get("apply_situation").strip()
        example= request.POST.get("example").strip()
        remark = request.POST.get("remark").strip()
        upload_time = datetime.date.today()

        status = ProductStatus.WAIT_SUBMIT
        maturity = Attribute.objects.get(id=maturity)
        independence = Attribute.objects.get(id=independence)
        business = Attribute.objects.get(id=business)
        technology = Attribute.objects.get(id=technology)
        attribute_num = maturity.first_class + independence.first_class + business.second_class + technology.second_class
        uploader = user
        is_vaild = False

        if pid != 0:
            product = Product.objects.get(id=pid)
            if product.status == ProductStatus.PASS:  # 单个更新
                product_old = Product.objects.get(product_num=product.product_num, version=product.version-1)
                product_old.is_vaild = False
                product_old.save()
                # apply_type = ApplyStatus.ALTER
                # version = product_old.version+1
            # else:  # 待提交修改和审核不通过修改
                # apply_type = product.apply_type
                # version = product.version

        else:  # 单个新建
            product = Product()
            product.save()
            product.product_num = product.id
            product.apply_type = ApplyStatus.NEW
            product.version = 1

        product.product_name = product_name
        product.old_product_name = old_product_name
        product.introduction = introduction
        product.is_overlap = is_overlap
        product.target_field = target_field
        product.apply_situation = apply_situation
        product.example = example
        product.one_year_money = one_year_money
        product.one_year_num = one_year_num
        product.three_year_money = three_year_money
        product.three_year_num = three_year_num
        product.pCompany = pCompany
        product.contact_people = contact_people
        product.remark = remark
        product.uploader = uploader
        product.upload_time = upload_time
        product.maturity = maturity
        product.independence = independence
        product.technology = technology
        product.business = business
        product.attribute_num = attribute_num
        product.status = status
        # product.apply_type = apply_type
        # product.version = version
        product.is_vaild = is_vaild
        product.save()

        if pid == 0:  # 新建上传的文件路径为temp/user
            path = os.path.join(TEMP_FILES_PATH, user.username)
            if os.path.exists(path) and os.listdir(path):
                file = os.listdir(path)[0]
                file_path = os.path.join(path, file)
                dest_path = os.path.join(PRODUCT_TEMP_ZIP_PATH, file)
                if not os.path.exists(PRODUCT_TEMP_ZIP_PATH):
                    os.makedirs(PRODUCT_TEMP_ZIP_PATH)
                shutil.move(file_path, dest_path)
                shutil.rmtree(path)
                product.real_name = os.path.splitext(file)[0].split('_')[0]+os.path.splitext(file)[1]
                product.save_name = file
                product.save()

    except Exception as e:
        if pid == 0 and product:
            product.delete()
        if product_old:
            product_old.is_vaild = True
            product_old.save()
        return ajax_error("产品提交失败:" + str(e))
    return ajax_success()


# 单个更新的时候先新建一个产品再跳转到该产品的编辑页
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_edit_product(request, pid):
    pid = int(pid)
    product = Product.objects.get(id = pid)
    product_new = Product()
    product_new.product_name = product.product_name
    product_new.old_product_name = product.old_product_name

    product_new.product_num = product.product_num
    product_new.introduction = product.introduction
    product_new.is_overlap = product.is_overlap
    product_new.target_field = product.target_field
    product_new.apply_situation = product.apply_situation
    product_new.example = product.example
    product_new.one_year_money = product.one_year_money
    product_new.one_year_num = product.one_year_num
    product_new.three_year_money = product.three_year_money
    product_new.three_year_num = product.three_year_num
    product_new.pCompany = product.pCompany
    product_new.maturity = product.maturity
    product_new.independence = product.independence
    product_new.business = product.business
    product_new.technology = product.technology
    product_new.attribute_num = product.attribute_num
    product_new.contact_people = product.contact_people
    product_new.remark = product.remark

    product_new.status = ProductStatus.PASS
    product_new.apply_type = ApplyStatus.ALTER
    product_new.version = product.version + 1
    product_new.is_vaild = False
    product_new.uploader = request.user.userprofile
    product_new.save()
    return HttpResponseRedirect("/product_management/edit_product/" + str(product_new.id) + "/")


# 取消提交操作
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def cancel_submit_product(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("取消失败!"+str(e))
    # 取消更新/新建
    if product.apply_type == ApplyStatus.NEW or product.apply_type == ApplyStatus.ALTER:
        file = product.save_name
        product.delete()
        if file:
            product_list = Product.objects.filter(save_name=file)
            print(product_list.count())
            if product_list.count() == 0:
                file_path = os.path.join(PRODUCT_TEMP_ZIP_PATH, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                files = os.listdir(PRODUCT_TEMP_EXCEL_PATH)
                for f in files:
                    if os.path.splitext(file)[0] in f:
                        file = f
                        break
                file_path = os.path.join(PRODUCT_TEMP_EXCEL_PATH, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    else:
        product.apply_type = ApplyStatus.FINISHED
        product.status = ProductStatus.PASS
        product.save()
    return ajax_success()


# 提交操作
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def submit_product(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("提交失败!"+str(e))
    product.status=ProductStatus.WAIT_PASS
    product.save()
    # 把文件从temp路径转移到正式路径
    file = product.save_name
    product_list = Product.objects.filter(save_name=file, status=ProductStatus.WAIT_SUBMIT)
    file_path = os.path.join(PRODUCT_TEMP_ZIP_PATH, file)
    dest_path = os.path.join(PRODUCT_ZIP_PATH, file)
    if os.path.isfile(file_path):
        if not os.path.exists(PRODUCT_ZIP_PATH):
            os.makedirs(PRODUCT_ZIP_PATH)
        if not product_list or len(product_list) == 0:
            shutil.move(file_path, dest_path)
        else:
            shutil.copy(file_path, dest_path)
    files = os.listdir(PRODUCT_TEMP_EXCEL_PATH)
    for f in files:
        if os.path.splitext(file)[0] in f:
            file = f
            break
    file_path = os.path.join(PRODUCT_TEMP_EXCEL_PATH, file)
    dest_path = os.path.join(PRODUCT_EXCEL_PATH, file)
    if os.path.isfile(file_path):
        if not os.path.exists(PRODUCT_EXCEL_PATH):
            os.makedirs(PRODUCT_EXCEL_PATH)
        if not product_list or len(product_list) == 0:
            shutil.move(file_path, dest_path)
        else:
            shutil.copy(file_path, dest_path)

    return ajax_success()


# 新建及更新页面“待审核”页签数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def wait_pass(request):
    fil = {"status": ProductStatus.WAIT_PASS}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# @login_required
# @permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
# def delete_file(request, file_name):
#     # 新建及更新页面“待审核”页面删除已上传文件
#     files = os.listdir(PRODUCT_TEMP_ZIP_PATH)
#     for file in files:
#         if re.search(file_name, file):
#             full_name = file
#             os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, full_name))
#             break
#     files = os.listdir(PRODUCT_TEMP_EXCEL_PATH)
#     for file in files:
#         if re.search(file_name, file):
#             full_name = file
#             os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, full_name))
#             break
#     product_list = Product.objects.filter(save_name__icontains=file_name)
#     for product in product_list:
#         product.save_name = None
#         product.real_name = None
#         product.save()
#     return HttpResponseRedirect("/product_management/page_new_product/")


# 新建及更新页面“已审核”页签数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def passed(request):
    fil = {"status__gte": ProductStatus.PASS}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil,order=["-status"])
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 待审核
@csrf_exempt
@login_required
@permission_required('webapp.product_information_manege_check')
def wait_check(request):
    fil = {"status": ProductStatus.WAIT_PASS}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)

# 通过审核操作
@csrf_exempt
@login_required
@permission_required('webapp.product_information_manege_check')
def check_product(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("审核失败!"+str(e))
    print(product.product_name)
    product.status=ProductStatus.PASS
    product.pass_time = datetime.date.today()
    product.reason=""
    # product.is_vaild=True
    a=product.pass_time
    b=product.apply_type
    if product.apply_type==ApplyStatus.NEW:
        product.is_vaild = True
        product.save()
    elif product.apply_type==ApplyStatus.ALTER:
        product_old=Product.objects.get(Q(product_num=product.product_num),Q(version=product.version-1),Q(is_vaild=True))
        product_old.is_vaild=False
        product_old.save()
        product.is_vaild = True
        product.save()
    elif product.apply_type==ApplyStatus.DELETE:
        product.delete()
    elif product.apply_type==ApplyStatus.INVALID:
        product.is_vaild = False
        product.save()

    return ajax_success()

# 已审核
@csrf_exempt
@login_required
@permission_required('webapp.product_information_manege_check')
def checked(request):
    fil = {"status__gte": ProductStatus.PASS}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)

# 不通过审核操作
@csrf_exempt
@login_required
@permission_required('webapp.product_information_manege_check')
def cancel_check_product(request):
    pid = request.POST.get('id')
    # reson=request.POST.get('reason')
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("不通过失败!"+str(e))
    product.status = ProductStatus.FAIL
    product.pass_time = datetime.date.today()
    product.reason=request.POST.get('reason')
    # if product.apply_type == ApplyStatus.ALTER:
    #     product_old = Product.objects.get(Q(product_num=product.product_num), Q(version=product.version - 1))
    #     if product_old:
    #         product_old.is_vaild = True
    #         product_old.save()
    #     product.save()
    # else:
    #     product.save()
    # a=product.reason
    # b=product.status
    product.save()
    return ajax_success()


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]