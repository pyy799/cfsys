from django.conf.urls import include, url
from django.contrib import admin
from webapp.attribute import views

urlpatterns = [
    # 属性管理
    url(r'^page_attribute/M/$', views.index, {"template_name": "attribute.html"}, name="page_M"),
    url(r'^page_attribute/I/$', views.index, {"template_name": "attribute.html"}, name="page_I"),
    url(r'^page_attribute/B/$', views.index, {"template_name": "attribute.html"}, name="page_B"),
    url(r'^page_attribute/T/$', views.index, {"template_name": "attribute.html"}, name="page_T"),
    #修改属性
    url(r'^page_attribute/[MIBT]/attribute_edit/$', views.attribute_edit, name="attribute_edit"),
    #增加分类
    url(r'^page_attribute/[MIBT]/add_attribute/$', views.add_attribute, name="add_attribute"),
    # url(r'^page_attribute/delete/(\d+)/$', views.del_class, name="del_class"),
    # url(r'^attribute_infor/data/$', views.attribute_infor, name="attribute_infor"),
    #修改大小类
    url(r'^page_attribute/[MIBT]/class_edit/$', views.class_edit, name="class_edit"),
    #删除大小类
    url(r'^page_attribute/[MIBT]/delete_class/$',views.delete_class,name="delete_class"),
    url(r'^page_attribute/[MIBT]/godelete_class/$',views.godelete_class,name="godelete_class"),
]