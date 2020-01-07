# coding=utf-8
import os
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from webapp import views
from django.contrib.staticfiles import views as gen_views


APPROOT = os.path.join(settings.BASE_DIR, "webapp")
urlpatterns = [
    url(r'^login/$', views.login_func, name='login'),
    url(r'^logout/$', views.logout_func, name='logout'),
    url(r'^findpassword/$',views.findpassword,name="findpassword"),
    url(r'^start_findpassword/$',views.start_findpassword,name="start_findpassword"),
    url(r'^check_email/$',views.check_email,name="check_email"),
    url(r'^reset_password/$',views.reset_password,name="reset_password"),
    url(r'^reset_password_success/$',views.reset_password_success,name="reset_password_success"),
    url(r'^userinformation/$',views.userinformation,name="userinformation"),
    url(r'^userinformation/ones_modify/$',views.ones_modify,name="ones_modify"),
    url(r'^userinformation/check_pd/$',views.check_pd,name="check_pd"),
    url(r'^userinformation/new_pd/$',views.new_pd,name="new_pd"),
    url(r'^$', RedirectView.as_view(url='/index/', permanent=True), name="default"),
    url(r'^index/$', views.index, {"template_name": "index.html"}, name="index"),
    url(r'^product_management/', include('webapp.product_management.urls')),
    url(r'^product_search/', include('webapp.product_search.urls')),
    url(r'^attribute/', include('webapp.attribute.urls')),
    url(r'^user/', include('webapp.user.urls')),
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}, name='static')
]
urlpatterns += static(settings.FILES_PATH, document_root=settings.FILES_PATH)

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$',
            gen_views.serve,
            {'document_root': os.path.join(APPROOT, 'static/')})
    ]

