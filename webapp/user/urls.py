from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    # 用户权限管理
    url(r'^page_user_management/$', views.index, {"template_name": "user_management.html"}, name="page_user_management"),
    url(r'^page_role_management/$', views.index, {"template_name": "role_management.html"}, name="page_role_management"),

]
