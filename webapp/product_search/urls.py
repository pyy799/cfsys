from django.conf.urls import include, url
from django.contrib import admin
from webapp import views
from webapp.product_search import views

urlpatterns = [
    # 产品查询页
    url(r'^page_search_product/$', views.index, {"template_name": "search_product.html"}, name="page_search_product"),
    # 属性化分类表
    url(r'^page_table/$', views.table, {"template_name": "table.html"}, name="page_table"),
    # 能力展示
    url(r'^page_show_product/$', views.show, {"template_name": "show_product.html"}, name="page_show_product"),
    # 能力展示页查询
    url(r'^page_show_product/search/$', views.search_show, {"template_name": "show_product.html"}, name="page_show_product_search"),
    # 能力展示页查询列表页
    url(r'^page_show_product/result/(?P<bid>\d+)/$', views.result, {"template_name": "show_product_result.html"},
        name="result"),
    # 查询
    url(r'^search/data/$', views.search, name="search"),
    # 产品详情
    url(r'^page_product_detail/(?P<bid>\d+)/$', views.detail,
        {"template_name": "product_detail.html"}, name="page_product_detail"),
    # url(r'^show/data/$', views.show, name="show"),
    # url(r'^page_product_detail/$', views.jump,
    #     {"template_name": "product_detail.html"}, name="page_product_detail"),
]
