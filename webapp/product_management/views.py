import os
import shutil

from django.http import HttpResponse
from django.shortcuts import render
from webapp.shortcuts.ajax import ajax_success, ajax_error
from cfsys.settings import *

def index(request, template_name):

    return render(request, template_name)


def jump(request, template_name):

    return render(request, template_name)


def page_new_product(request, template_name):
    page_dict = {}

    excel_name = "template.xlsx"
    download_path_excel = os.path.join(FILES_PATH, excel_name)
    page_dict.update({"download_path_excel": download_path_excel, "excel_name": excel_name})

    return render(request, template_name, page_dict)


def upload_many(request):
    if request.method != "POST":
        return ajax_error("上传失败")

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



    zip = request.FILES.get("zip", None)  # 获取上传的文件，如果没有文件，则默认为None
    # path = os.path.join(PRODUCT_ZIP_PATH, temp_user_company)  # 临时存储路径为zip/companyname
    path = os.path.join(PRODUCT_ZIP_PATH)  # 临时存储路径为zip/companyname
    if not os.path.exists(path):
        os.makedirs(path)
    destination = open(os.path.join(path, zip.name), "wb+")  # 把文件写入
    for chunk in zip.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return ajax_success()