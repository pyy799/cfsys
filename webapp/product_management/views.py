
import os
import re
import shutil
import time
import xlrd
from django.contrib.auth.decorators import login_required
from webapp.shortcuts.decorator import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from webapp.models import *
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *
from webapp.utils.query import get_query, create_data


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
    page_dict.update({"company_choice": company_choice, "apply_choice": apply_choice})

    return render(request, template_name, page_dict)

# 更新页面数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def update_data(request):
    fil = {"status": ProductStatus.PASS, "is_vaild": True}
    # 只能看到自己公司的
    user = request.user.userprofile
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
        return ajax_error("停用失败!")
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
        return ajax_error("取消失败!")
    product.apply_type = ApplyStatus.DELETE
    product.status = ProductStatus.WAIT_SUBMIT
    product.save()
    return ajax_success()


# 新建及更新页面“待提交”页签数据
@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def wait_submit(request):
    fil = {"status": ProductStatus.WAIT_SUBMIT, "is_vaild": True}
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
    now = int(time.time())
    if request.method != "POST":
        return ajax_error("上传失败")
    zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
    save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
    save_zip = os.path.splitext(zip.name)[1]
    zip_file_name = save_name+save_zip
    if not os.path.exists(PRODUCT_TEMP_ZIP_PATH):
        os.makedirs(PRODUCT_TEMP_ZIP_PATH)
    destination = open(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name), "wb+")  # 把文件写入
    for chunk in zip.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    excel = request.FILES.get("excel", None)  # 获取上传的文件，如果没有文件，则默认为None
    save_excel = os.path.splitext(excel.name)[1]
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
    product_list = []
    try:
        for i in range(1, nrows):
            row = sheet.row_values(i)
            product_name = str(row[0]).strip()
            product_exist = Product.objects.filter(product_name=product_name, is_vaild=True)
            if len(product_exist)>0:
                for product in product_list:
                    product.delete()
                os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name))
                os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name))
                return ajax_error("产品名称重复！")
            old_product_name = str(row[1]).strip()
            if old_product_name == 'N.A.':
                old_product_name = None
            introduction = str(row[2]).strip()
            overlap = str(row[3]).strip()
            if overlap=="是":
                is_overlap = True
            else:
                is_overlap = False
            target_field = str(row[4]).strip()
            apply_situation = str(row[5]).strip()
            example = str(row[6]).strip()
            one_year_money = float(row[7])
            one_year_num = int(re.findall(r"\d+", row[8].strip())[0])
            three_year_money = float(row[9])
            three_year_num = int(re.findall(r"\d+", row[10].strip())[0])
            pCompany = str(row[11]).strip()
            pCompany = int(get_key(dict(COMPANY_CHOICE),pCompany)[0])
            maturity = str(row[12]).strip()
            independence = str(row[13]).strip()
            business = str(row[14]).strip()
            technology = str(row[15]).strip()
            contact_people = str(row[16]).strip()
            remark = str(row[17]).strip()
            upload_time = datetime.date.today()
            real_name = zip.name

            attribute_num = maturity+independence+business+technology
            status = ProductStatus.WAIT_SUBMIT
            apply_type = ApplyStatus.NEW
            version = 1
            is_vaild = True

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
            product.maturity = Attribute.objects.get(first_class=maturity)
            product.independence = Attribute.objects.get(first_class=independence)
            product.business = Attribute.objects.get(second_class=business)
            product.technology = Attribute.objects.get(second_class=technology)
            product.attribute_num = attribute_num
            product.status = status
            product.apply_type = apply_type
            product.version = version
            product.is_vaild = is_vaild
            product.save()
    except Exception as e:
        for product in product_list:
            product.delete()
        os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, zip_file_name))
        os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, excel_file_name))
        return ajax_error("产品内容有误!")

    # '产品名称', '旧产品名称', '产品描述', '是否重叠', '目标行业', '应用场景', '市场案例', '过去一年销售额（万元）',
    # '过去一年销售数量（套/件/组）', '过去三年销售数量（万元）', '过去三年销售数量（套/件/组）', '公司', 'M\n（成熟度）',
    # 'I\n（自主度）', 'B\n（业务类别）', 'T\n（技术形态）', '联系人及联系方式', '备注'

    return ajax_success()


# 新建/修改产品页面
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_product(request, pid, template_name):
    user = request.user.userprofile
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
            file_name = real_name   # 如果是修改或更新，则原文件在temp路径
        except Exception as e:
            return ajax_error("产品不存在!")

    else:  # 新建
        path = os.path.join(TEMP_FILES_PATH, user.username)   # 如果是新建，则原文件在temp/user路径
        if os.path.exists(path) and len(os.listdir(path)):
            file_name = os.listdir(path)[0].split('_')[0]
    page_dict = {"pid": pid, "product": product_value, "file_name": file_name, "company_choice": company_choice,
                 "m_choice": m_choice, "i_choice": i_choice, "b_choice":b_choice, "t_choice":t_choice}
    return render(request, template_name, page_dict)


# 编辑产品页面上传文件
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_upload_file(request, pid):
    user = request.user.userprofile
    now = int(time.time())
    pid = int(pid)
    if pid != 0:  # 修改或更新
        product = Product.objects.get(id=pid)
        if request.method != "POST":
            return ajax_error("上传失败")
        zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
        print(save_name)
        save_zip = os.path.splitext(zip.name)[1]
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
            return ajax_error("上传失败")
        zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
        save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
        save_zip = os.path.splitext(zip.name)[1]
        zip_file_name = save_name+save_zip
        path = os.path.join(TEMP_FILES_PATH, user.username)
        if not os.path.exists(path):
            os.makedirs(path)
        destination = open(os.path.join(path, zip_file_name), "wb+")  # 把文件写入
        for chunk in zip.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
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
            if len(product_list)==0:  # 如果还有关联产品就不删
                if status == ProductStatus.WAIT_SUBMIT:
                    os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, full_name))
                else:
                    os.remove(os.path.join(PRODUCT_ZIP_PATH, full_name))
            product.save_name = None
            product.real_name = None
            product.save()
        except Exception as e:
            return ajax_error("找不到产品!")
    else:  # 新建-编辑-删文件
        path = os.path.join(TEMP_FILES_PATH, user.username)
        if os.path.exists(path):
            shutil.rmtree(path)

    return HttpResponseRedirect("/product_management/edit_product/"+str(pid)+"/")


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_submit(request, pid):
    # 编辑产品页面提交
    user = request.user.userprofile
    pid = int(pid)
    product_name = request.POST.get("product_name")
    product_list = Product.objects.filter(product_name=product_name, is_vaild=True)
    count = len(product_list)
    if count > 0:
        return HttpResponse("产品名称已存在!")
    old_product_name = request.POST.get("old_product_name")
    pCompany = request.POST.get("pCompany")
    is_overlap = request.POST.get("is_overlap")
    maturity = request.POST.get("maturity") or ''
    independence = request.POST.get("independence") or ''
    business = request.POST.get("business") or ''
    technology = request.POST.get("technology") or ''
    one_year_money= float(request.POST.get("one_year_money") or 0)
    one_year_num= int(request.POST.get("one_year_num") or 0)
    three_year_money = float(request.POST.get("three_year_money") or 0)
    three_year_num= int(request.POST.get("three_year_num") or 0)
    contact_people= request.POST.get("contact_people")
    introduction= request.POST.get("introduction")
    target_field = request.POST.get("target_field")
    apply_situation = request.POST.get("apply_situation")
    example= request.POST.get("example")
    remark = request.POST.get("remark")
    upload_time = datetime.date.today()
    status = ProductStatus.WAIT_SUBMIT
    attribute_num = maturity + independence + business + technology
    uploader = user
    is_vaild = True

    if pid != 0:
        product_old = Product.objects.get(id=pid)
        if product_old.status == ProductStatus.PASS:  # 单个更新
            product_old = Product.objects.get(id=pid)
            product_old.is_vaild = False
            product_old.save()
            product = Product()
            product.save()
            product.product_num = product_old.product_num
            product.apply_type = ApplyStatus.ALTER
            product.version = product_old.version+1
        else:  # 待提交修改和审核不通过修改
            product = product_old

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
    if maturity:
        product.maturity = Attribute.objects.get(id=maturity)
    if independence:
        product.independence = Attribute.objects.get(id=independence)
    if technology:
        product.technology = Attribute.objects.get(id=technology)
    if business:
        product.business = Attribute.objects.get(id=business)
    product.attribute_num = attribute_num
    product.status = status
    # product.apply_type = apply_type
    # product.version = version
    product.is_vaild = is_vaild
    product.save()
    file_name = request.POST.get("file_name")
    if file_name!='[]' and file_name:
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

    return HttpResponseRedirect("/product_management/page_new_product/")


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def cancel_submit_product(request, pid):
    # 取消提交操作
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("取消失败!")
    # 取消更新/新建
    if product.apply_type == ApplyStatus.NEW or product.apply_type == ApplyStatus.ALTER:
        file = product.save_name
        product_list = Product.objects.filter(save_name=file)
        if not product_list or len(product_list)==0:
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
        product.delete()
    else:
        product.apply_type = ApplyStatus.FINISHED
        product.status = ProductStatus.PASS
        product.save()
    return ajax_success()


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def submit_product(request, pid):
    # 提交操作
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        return ajax_error("提交失败!")
    print(product.product_name)
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


@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def wait_pass(request):
    # 新建及更新页面“待审核”页签数据
    fil = {"status": ProductStatus.WAIT_PASS, "is_vaild": True}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)

#
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
    fil = {"status__gte": ProductStatus.PASS, "is_vaild": True}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]