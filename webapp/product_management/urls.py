from django.conf.urls import include, url
from django.contrib import admin
from webapp.product_management import views

urlpatterns = [
    # 信息管理
    url(r'^page_new_product/$', views.page_new_product, {"template_name": "new_product.html"}, name="page_new_product"),
    url(r'^page_pass_product/$', views.index, {"template_name": "pass_product.html"}, name="page_pass_product"),
    url(r'^page_table/$', views.jump, {"template_name": "table.html"}, name="page_table"),
    url(r'^upload_many/$', views.upload_many, name="upload_many"),
]
