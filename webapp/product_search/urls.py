from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    # 产品查询
    url(r'^page_search_product/$', views.index, {"template_name": "search_product.html"}, name="page_search_product"),
    url(r'^page_show_product/$',views.index,{"template_name" : "show_product.html"},name="page_show_product"),
]
