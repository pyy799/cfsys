from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from webapp.models import UserProfile,Group


def index(request, template_name):

    return render(request, template_name)


@login_required
@permission_required(['webapp.user_right_management_user',''])
def jump(request, template_name):
    users = UserProfile.objects.all()
    groups = Group.objects.all()
    for user in users:
        user.date_joined = user.date_joined.strftime('%Y-%m-%d')
        user.Company = user.get_company(user.uCompany)
        qs = Group.objects.get(user=user)
        user.group = qs.name
    return render(request, template_name, {"users": users, "groups":groups})


@login_required
@permission_required('webapp.user_right_management_user')
def add_user(request):
    username = request.POST.get("add_name")
    gender = request.POST.get("add_gender")
    uCompany = request.POST.get("add_company")
    department = request.POST.get("add_department")
    position = request.POST.get("add_position")
    role = request.POST.get("add_role")
    phone = request.POST.get("add_phone")
    email = request.POST.get("add_email")
    UserProfile.objects2.create_user(username=username, password="123456",
                    gender=gender, uCompany=uCompany, department=department,
                    position=position, role=role, phone=phone, email=email)

    return HttpResponseRedirect('/user/page_user_management/')


@login_required
@permission_required('webapp.user_right_management_user')
def delete_user(request, delete_id):
    UserProfile.objects.filter(id=delete_id).delete()
    return HttpResponseRedirect('/user/page_user_management/')