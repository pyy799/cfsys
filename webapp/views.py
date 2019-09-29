from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from webapp.shortcuts.ajax import ajax_success, ajax_error
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from webapp.upattribute import import_attribute


def index(request, template_name):
    # import_attribute()
    return render(request, template_name)


@login_required
def jump(request, template_name):

    return render(request, template_name)


@never_cache
def login_func(request):
    """登录"""
    if request.method == "GET":
        form = AuthenticationForm(request)
        return TemplateResponse(request, 'login.html', {'form': form})
    elif request.method == "POST":
        try:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                return ajax_success()
            else:
                return ajax_error("dsf")
        except:
            return ajax_error("dsf")


@login_required
def logout_func(request):
    logout(request)
    return HttpResponse('欢迎下次光临!')
