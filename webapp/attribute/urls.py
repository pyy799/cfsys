from django.conf.urls import include, url
from django.contrib import admin
from webapp.attribute import views

urlpatterns = [
    # 属性管理
    url(r'^page_attribute/$', views.index, {"template_name": "attribute.html"}, name="page_attribute"),
    # url(r'^attribute_infor/data/$', views.attribute_infor, name="attribute_infor"),
]
