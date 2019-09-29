import os
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from webapp import views


APPROOT = os.path.join(settings.BASE_DIR, "webapp")
urlpatterns = [
    url(r'^login/$', views.login_func, name='login'),
    url(r'^logout/$', views.logout_func, name='logout'),
    url(r'^$', RedirectView.as_view(url='/index/', permanent=True), name="default"),
    url(r'^index/$', views.index, {"template_name": "index.html"}, name="index"),
    url(r'^product_management/', include('webapp.product_management.urls')),
    url(r'^product_search/', include('webapp.product_search.urls')),
    url(r'^attribute/', include('webapp.attribute.urls')),
    url(r'^user/', include('webapp.user.urls')),
]
urlpatterns += static(settings.FILES_PATH, document_root=settings.FILES_PATH)

