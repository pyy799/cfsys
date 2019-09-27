import os
import re
import shutil
import datetime
import xlrd
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
def page_new_product(request, template_name):
    page_dict = {}
    template_file = "template.xlsx"
    download_path_excel = os.path.join(FILES_PATH, template_file)
    company_choice = COMPANY_CHOICE
    apply_choice = APPLY_CHOICE
    page_dict.update({"download_path_excel": download_path_excel, "excel_name": template_file,
                      "company_choice": company_choice, "apply_choice": apply_choice})

    return render(request, template_name, page_dict)

@csrf_exempt
# 新建及更新页面“待提交”页签数据
def wait_submit(request):
    fil = {"status": ProductStatus.WAIT_SUBMIT, "is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


# 批量上传
def upload_many(request):
    if request.method != "POST":
        return ajax_error("上传失败")

    zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
    # path = os.path.join(PRODUCT_ZIP_PATH, temp_user_company)  # 临时存储路径为zip/companyname
    path = os.path.join(PRODUCT_ZIP_PATH)  # 临时存储路径为zip/companyname
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(os.path.join(path, zip.name), "wb+")  # 把文件写入
    for chunk in zip.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    excel = request.FILES.get("excel", None)  # 获取上传的文件，如果没有文件，则默认为None
    # temp_user_company = request.user.userprofile.uCompany
    # path = os.path.join(PRODUCT_EXCEL_PATH, temp_user_company)  # 存储路径为excel/companyname
    path = os.path.join(PRODUCT_EXCEL_PATH)  # 存储路径为excel/companyname
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(os.path.join(path, excel.name), "wb+")  # 把文件写入
    for chunk in excel.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    file = os.path.join(path, excel.name)
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
        save_name = zip.name.split('.')[1]
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
        # product.uploader
        product.upload_time = upload_time
        product.real_name = real_name
        product.save_name = str(product.product_num)+'_'+str(version)+'.'+save_name
        # product.maturity
        # product.independence
        # product.business
        # product.technology
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


# 新建/修改产品页面
def edit_product(request, pid, template_name):
    pid = int(pid)
    if pid != 0 :
        try:
            product = Product.objects.get(id=pid)
        except Exception as e:
            # log.log_error("审批通过：找不到合同！\n%s" % e)
            return ajax_error("审批失败!")


    page_dict = {"pid": pid}
    return render(request, template_name, page_dict)


# 取消提交操作
def cancel_submit_product(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        # log.log_error("审批通过：找不到合同！\n%s" % e)
        return ajax_error("取消失败!")
    print(product.product_name)
    product.delete()
    return ajax_success()


# 提交操作
def submit_product(request, pid):
    try:
        product = Product.objects.get(id=pid)
    except Exception as e:
        # log.log_error("审批通过：找不到合同！\n%s" % e)
        return ajax_error("提交失败!")
    print(product.product_name)
    product.status=ProductStatus.WAIT_PASS
    product.save()
    return ajax_success()


@csrf_exempt
# 新建及更新页面“待审核”页签数据
def wait_pass(request):
    fil = {"status": ProductStatus.WAIT_PASS, "is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


@csrf_exempt
# 新建及更新页面“已审核”页签数据
def passed(request):
    fil = {"status__gte": ProductStatus.PASS, "is_vaild": True}
    product_list, count, error = get_query(request, Product, **fil)
    pack_list = [i.pack_data() for i in product_list]
    res = create_data(request.POST.get("draw", 1), pack_list, count)
    return HttpResponse(res)


def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]