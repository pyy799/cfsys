from django.conf.urls import include, url
from django.contrib import admin
from webapp import views
from webapp.product_search import views

urlpatterns = [
    # 产品查询页
    url(r'^page_search_product/$', views.index, {"template_name": "search_product.html"}, name="page_search_product"),
    # 查询
    url(r'^search/data/$', views.search, name="search"),

    # 能力展示
    url(r'^page_show_product/$', views.show, {"template_name": "show_product.html"}, name="page_show_product"),
    # # 能力展示页查询
    # url(r'^page_show_product/search/$', views.search_show, {"template_name": "show_product.html"},
    #     name="page_show_product_search"),
    #图表产品列表
    url(r'^page_chart_product_list/$',views.chart_list,{"template_name":"chart_product_list.html"},name="page_chart_product_list"),
    # # 图表产品列表返回展示查询结果
    # url(r'^list_return_show/$', views.show, name="list_return_show"),
    # # 能力展示页查询列表页
    # url(r'^page_show_product/result/$', views.result, {"template_name": "show_product_result.html"},
    #     name="result"),


    # # 图表产品查询页
    # url(r'^page_show_product_result/$', views.show_index, {"template_name": "show_product_result.html"},
    #     name="page_show_product_result"),
    # # 图表查询
    # url(r'^show/data/$', views.show_data, name="show_data"),

    # 产品详情
    url(r'^page_product_detail/(?P<bid>\d+)/$', views.detail,
        {"template_name": "product_detail.html"}, name="page_product_detail"),
    # 属性化分类表
    url(r'^page_table/$', views.table, {"template_name": "table.html"}, name="page_table"),

    # url(r'^show/data/$', views.show, name="show"),
    # url(r'^page_product_detail/$', views.jump,
    #     {"template_name": "product_detail.html"}, name="page_product_detail"),
]
