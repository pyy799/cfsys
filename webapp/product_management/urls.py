from django.conf.urls import include, url
from webapp.product_management import views

urlpatterns = [
    # 信息管理
    # 新建及更新-新建
    url(r'^page_new_product/$', views.page_new_product, {"template_name": "new_product.html"}, name="page_new_product"),
    url(r'^page_update_product/$', views.page_new_product, {"template_name": "new_product.html"}, name="page_update_product"),

    url(r'^new_many/$', views.new_many, name="new_many"),
    url(r'^update_many/$', views.update_many, name="update_many"),
    # 更新
    url(r'^update/data/$', views.update_data, name="update_data"),
    url(r'^update/invalid/(?P<pid>\d+)/$', views.update_invalid, name="update_invalid"),
    url(r'^update/delete/(?P<pid>\d+)/$', views.update_delete, name="update_delete"),
    # 编辑详情
    url(r'^edit_product/(?P<pid>\d+)/$', views.edit_product, {"template_name": "edit_product.html"}, name="edit_product"),
    url(r'^edit_product/delete_file/(?P<pid>\d+)/$', views.edit_delete_file, name="edit_delete_file"),
    url(r'^edit_product/upload/(?P<pid>\d+)/$', views.edit_upload_file, name="edit_upload_product"),
    url(r'^edit_product/submit/(?P<pid>\d+)/$', views.edit_submit, name="edit_submit"),

    # 新建及更新-待提交
    url(r'^wait_submit/data/$', views.wait_submit, name="wait_submit"),
    url(r'^wait_submit/cancel/(?P<pid>\d+)/$', views.cancel_submit_product, name="cancel_submit_product"),
    url(r'^wait_submit/submit/(?P<pid>\d+)/$', views.submit_product, name="submit_product"),
    # url(r'^wait_submit/delete_file/(?P<file_name>\w+)/$', views.delete_file, name="delete_file"),

    # 新建及更新-待审核
    url(r'^wait_pass/data/$', views.wait_pass, name="wait_pass"),
    # 新建及更新-已审核
    url(r'^passed/data/$', views.passed, name="passed"),

    # 审核
    url(r'^page_pass_product/$', views.index, {"template_name": "pass_product.html"}, name="page_pass_product"),
    # 待审核
    url(r'^wait_check/data/$', views.wait_check, name="wait_check"),
    url(r'^wait_check/check/(?P<pid>\d+)/$', views.check_product, name="check_product"),
    url(r'^wait_check/cancel/$', views.cancel_check_product, name="cancel_check_product"),
    #已审核
    url(r'^checked/data/$', views.checked, name="checked"),
]
