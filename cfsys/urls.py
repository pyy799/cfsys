from django.conf.urls import include, url
from django.contrib import admin
from webapp import views

urlpatterns = [
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
]
