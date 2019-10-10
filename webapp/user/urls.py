from django.conf.urls import include, url
from django.contrib import admin
from webapp.user import views

urlpatterns = [
    # 用户权限管理
    url(r'^page_user_management/$', views.jump, {"template_name": "user_management.html"}, name="page_user_management"),
    url(r'^page_user_management/add_user/$', views.add_user, name="add_user"),
    url(r'^page_user_management/delete/(\d+)/$', views.delete_user, name="delete_user"),
    url(r'^page_role_management/$', views.index, {"template_name": "role_management.html"}, name="page_role_management"),
    url(r'^page_user_management/active$', views.active_user, name="active_user"),
    url(r'^page_user_management/modify/$', views.modify_user, name="modify_user"),
    url(r'^page_user_management/search/$', views.search_user, name="search_user")
]
