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


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def page_new_product(request, template_name):
    # 新建及更新页面
    page_dict = {}
    user = request.user.userprofile
    file_names = []
    if os.path.exists(PRODUCT_TEMP_ZIP_PATH):
        files = os.listdir(PRODUCT_TEMP_ZIP_PATH)
        for i in files:
            if re.search(user.username, i) and i.split('.')[0]:
                file_names.append([i.split('_')[0], i.split('.')[0]])
    template_file = "template.xlsx"
    download_path_excel = os.path.join(FILES_PATH, template_file)
    company_choice = COMPANY_CHOICE
    apply_choice = APPLY_CHOICE

    page_dict.update({"download_path_excel": download_path_excel, "excel_name": template_file,
                      "company_choice": company_choice, "apply_choice": apply_choice, "file_names":file_names})

    return render(request, template_name, page_dict)


@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def wait_submit(request):
    # 新建及更新页面“待提交”页签数据
    fil = {"status": ProductStatus.WAIT_SUBMIT, "is_vaild": True}
    # 只能看到自己的
    user = request.user.userprofile
    fil.update({"uploader": user})
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def upload_many(request):
    # 批量新建
    user = request.user.userprofile
    now = int(time.time())
    if request.method != "POST":
        return ajax_error("上传失败")
    zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
    save_name = os.path.splitext(zip.name)[0] + '_' + user.username + '_' + str(now)
    save_zip = os.path.splitext(zip.name)[1]
    zip_file_name = save_name+'.'+save_zip
    path = PRODUCT_TEMP_ZIP_PATH
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(os.path.join(path, zip_file_name), "wb+")  # 把文件写入
    for chunk in zip.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    excel = request.FILES.get("excel", None)  # 获取上传的文件，如果没有文件，则默认为None
    save_excel = os.path.splitext(excel.name)[1]
    excel_file_name = save_name+'.'+save_excel
    path = os.path.join(PRODUCT_TEMP_EXCEL_PATH)
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(os.path.join(path, excel_file_name), "wb+")  # 把文件写入
    for chunk in excel.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    file = os.path.join(path, excel_file_name)
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name("产品信息页")
    nrows = sheet.nrows

    for i in range(1, nrows):
        row = sheet.row_values(i)
        product_name = row[0].strip()
        old_product_name = row[1].strip()
        if old_product_name == 'N.A.':
            old_product_name = None
        introduction = row[2].strip()
        overlap = row[3].strip()
        if overlap=="是":
            is_overlap = True
        else:
            is_overlap = False
        target_field = row[4].strip()
        apply_situation = row[5].strip()
        example = row[6].strip()
        one_year_money = float(row[7])
        one_year_num = int(re.findall(r"\d+", row[8].strip())[0])
        three_year_money = float(row[9])
        three_year_num = int(re.findall(r"\d+", row[10].strip())[0])
        pCompany = row[11].strip()
        pCompany = int(get_key(dict(COMPANY_CHOICE),pCompany)[0])
        maturity = row[12].strip()
        independence = row[13].strip()
        business = row[14].strip()
        technology = row[15].strip()
        contact_people = row[16].strip()
        remark = row[17].strip()
        upload_time = datetime.date.today()
        real_name = zip.name

        attribute_num = maturity+independence+business+technology
        status = ProductStatus.WAIT_SUBMIT
        apply_type = ApplyStatus.NEW
        version = 1
        is_vaild = True

        product = Product()
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
    # '产品名称', '旧产品名称', '产品描述', '是否重叠', '目标行业', '应用场景', '市场案例', '过去一年销售额（万元）',
    # '过去一年销售数量（套/件/组）', '过去三年销售数量（万元）', '过去三年销售数量（套/件/组）', '公司', 'M\n（成熟度）',
    # 'I\n（自主度）', 'B\n（业务类别）', 'T\n（技术形态）', '联系人及联系方式', '备注'

    return ajax_success()


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def edit_product(request, pid, template_name):
    # 新建/修改产品页面
    pid = int(pid)
    if pid != 0 :
        try:
            product = Product.objects.get(id=pid)
        except Exception as e:
            # log.log_error("审批通过：找不到合同！\n%s" % e)
            return ajax_error("审批失败!")

    page_dict = {"pid": pid}
    return render(request, template_name, page_dict)


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def cancel_submit_product(request, pid):
    # 取消提交操作
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        # log.log_error("审批通过：找不到合同！\n%s" % e)
        return ajax_error("取消失败!")
    # 删除上传的文件
    file = product.save_name
    product_list = Product.objects.filter(save_name=file)
    if not product_list:
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
    return ajax_success()


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def submit_product(request, pid):
    # 提交操作
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        # log.log_error("审批通过：找不到合同！\n%s" % e)
        return ajax_error("提交失败!")
    print(product.product_name)
    product.status=ProductStatus.WAIT_PASS
    product.save()
    # 把文件从temp路径转移到正式路径
    file = product.save_name
    file_path = os.path.join(PRODUCT_TEMP_ZIP_PATH, file)
    dest_path = os.path.join(PRODUCT_ZIP_PATH, file)
    if os.path.isfile(file_path):
        shutil.move(file_path, dest_path)
    files = os.listdir(PRODUCT_TEMP_EXCEL_PATH)
    for f in files:
        if os.path.splitext(file)[0] in f:
            file = f
            break
    file_path = os.path.join(PRODUCT_TEMP_EXCEL_PATH, file)
    dest_path = os.path.join(PRODUCT_EXCEL_PATH, file)
    if os.path.isfile(file_path):
        shutil.move(file_path, dest_path)

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


@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def delete_file(request, file_name):
    # 新建及更新页面“待审核”页面删除已上传文件
    files = os.listdir(PRODUCT_TEMP_ZIP_PATH)
    for file in files:
        if re.search(file_name, file):
            full_name = file
            os.remove(os.path.join(PRODUCT_TEMP_ZIP_PATH, full_name))
            break
    files = os.listdir(PRODUCT_TEMP_EXCEL_PATH)
    for file in files:
        if re.search(file_name, file):
            full_name = file
            os.remove(os.path.join(PRODUCT_TEMP_EXCEL_PATH, full_name))
            break
    product_list = Product.objects.filter(save_name__icontains=file_name)
    for product in product_list:
        product.save_name = None
        product.real_name = None
        product.save()
    return HttpResponseRedirect("/product_management/page_new_product/")

@csrf_exempt
@login_required
@permission_required(['webapp.product_information_manage_new', 'webapp.product_information_manage_update'])
def passed(request):
    # 新建及更新页面“已审核”页签数据
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