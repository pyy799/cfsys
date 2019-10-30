from django.conf.urls import include, url
from webapp.product_search import views

urlpatterns = [
    # 产品查询页
    url(r'^page_search_product/$', views.index, {"template_name": "search_product.html"}, name="page_search_product"),

    # 查询
    url(r'^search/data/$', views.search, name="search"),

    # 能力展示
    url(r'^page_show_product/$', views.show, {"template_name": "show_product.html"}, name="page_show_product"),

    #图表产品列表
    url(r'^page_chart_product_list/$',views.chart_list,{"template_name":"chart_product_list.html"},name="page_chart_product_list"),

    # 产品详情
    url(r'^page_product_detail/(?P<bid>\d+)/$', views.detail,
        {"template_name": "product_detail.html"}, name="page_product_detail"),

    # 属性化分类表
    url(r'^page_table/$', views.table, {"template_name": "table.html"}, name="page_table"),
]
