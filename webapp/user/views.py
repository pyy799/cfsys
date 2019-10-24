from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from webapp.models import UserProfile, Group, GroupCom
from django.contrib.auth.models import Permission
import json

@login_required
@permission_required('webapp.user_right_management_user')
def jump_user(request, template_name):
    page = 1
    pageLimit = 2
    userCounts = UserProfile.objects.all().count()
    if userCounts % pageLimit != 0:
        pageCounts = int(userCounts/pageLimit)+1
    else:
        pageCounts = int(userCounts/pageLimit)
    users = UserProfile.objects.all().order_by("-id")[(page-1)*pageLimit:page*pageLimit]
    groups = Group.objects.all().order_by("id")
    for user in users:
        user.date_joined = user.date_joined.strftime('%Y-%m-%d')
        user.Company = user.get_company(user.uCompany)
        gr = Group.objects.get(user=user)
        user.group = gr.name
    return render(request, template_name, {"users": users, "groups": groups, "pageCounts": pageCounts})


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


@csrf_exempt
@login_required
@permission_required('webapp.user_right_management_user')
def active_user(request):
    active_id = request.GET.get("active_id")
    user = UserProfile.objects.get(id=active_id)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({"active": user.is_active})


@csrf_exempt
@login_required
@permission_required('webapp.user_right_management_user')
def modify_user(request):
    # 判断数据库中是否已经存在该用户名称
    userCount = UserProfile.objects.filter(username=request.POST.get("username").strip()).count()
    if userCount > 1:
        return JsonResponse({"status": -1})
    modify_id = request.POST.get("id")
    user = UserProfile.objects.get(id=modify_id)
    user.username = request.POST.get("username").strip()
    user.gender = request.POST.get("gender")
    user.uCompany = request.POST.get("uCompany")
    user.department = request.POST.get("department")
    user.position = request.POST.get("position")
    user.phone = request.POST.get("phone")
    user.email = request.POST.get("email")
    user.save()

    gr = Group.objects.get(user=user)
    user.groups.remove(gr)
    group = Group.objects.get(id=request.POST.get("role"))
    user.groups.add(group)
    user = UserProfile.objects.get(id=modify_id)
    res = {
        "username": user.username,
        "gender": user.gender,
        "Company": user.get_company(user.uCompany),
        "department": user.department,
        "position": user.position,
        "group": group.name,
        "phone": user.phone,
        "email": user.email,
        "status": 0
    }
    return JsonResponse(res)


@csrf_exempt
@login_required
@permission_required('webapp.user_right_management_user')
def search_user(request):
    # 获得页数
    page = int(request.POST.get("page"))
    pageLimit = 2
    # 获得查询条件
    username = request.POST.get("username")
    uCompany = request.POST.get("uCompany")
    department = request.POST.get("department")
    position = request.POST.get("position")
    group = request.POST.get("group")
    search_dict = dict()
    if username.strip() != "":
        search_dict["username__contains"] = username
    if uCompany != '0':
        search_dict["uCompany"] = int(uCompany)
    if department.strip() != "":
        search_dict["department__contains"] = department
    if position.strip() != "":
        search_dict["position__contains"] = position
    if group != '0':
        search_dict["groups__id"] = int(group)
    print(search_dict)
    if not search_dict:
        userCounts = UserProfile.objects.all().count()
    else:
        userCounts = UserProfile.objects.filter(**search_dict).count()
    if userCounts % pageLimit != 0:
        pageCounts = int(userCounts/pageLimit)+1
    else:
        pageCounts = int(userCounts/pageLimit)
    if not search_dict:
        user_set = UserProfile.objects.all().order_by("-id")[(page-1)*pageLimit:page*pageLimit]
    else:
        user_set = UserProfile.objects.filter(**search_dict).order_by("-id")[(page-1)*pageLimit:page*pageLimit]
    data_list = []
    for user in user_set:
        gr = Group.objects.get(user=user)
        user_dict = {
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "Company": user.get_company(user.uCompany),
            "department": user.department,
            "position": user.position,
            "group": gr.name,
            "phone": user.phone,
            "email": user.email,
            "date_joined": user.date_joined.strftime('%Y-%m-%d'),
            "is_active": user.is_active,
        }
        data_list.append(user_dict)
    return JsonResponse({"status": 0, "users": data_list,"pageCounts": pageCounts,"userCounts": userCounts})


@login_required
@permission_required('webapp.user_right_management_role')
def jump_role(request, template_name):
    group_set = Group.objects.all().order_by("id")
    group_list = []
    for group in group_set:
        perm_list = []
        permissions = group.permissions.all()
        for permission in permissions:
            perm_list.append(permission.codename)
        group_dic = {"id": group.id, "name": group.name, "perm_list":perm_list}
        group_list.append(group_dic)
    # return JsonResponse({"group_list":group_list})
    return render(request, template_name, {"group_list": group_list})


@login_required
@permission_required('webapp.user_right_management_role')
def add_role(request):
    group_name = request.POST.get("group_name").strip()
    groupCount = Group.objects.filter(name=group_name).count()
    if groupCount != 0:
        return JsonResponse({"status": -1})
    group = Group()
    group.name = group_name
    group.save()
    perm_list = []
    if request.POST.get("perm1") == "true":
        permission = Permission.objects.get(codename="product_information_inquiry")
        perm_list.append("product_information_inquiry")
        group.permissions.add(permission)
    if request.POST.get("perm2") == "true":
        permission = Permission.objects.get(codename="product_information_manage_new")
        perm_list.append("product_information_manage_new")
        group.permissions.add(permission)
    if request.POST.get("perm3") == "true":
        permission = Permission.objects.get(codename="product_information_manage_update")
        perm_list.append("product_information_manage_update")
        group.permissions.add(permission)
    if request.POST.get("perm4") == "true":
        permission = Permission.objects.get(codename="product_information_manege_check")
        perm_list.append("product_information_manege_check")
        group.permissions.add(permission)
    if request.POST.get("perm5") == "true":
        permission = Permission.objects.get(codename="product_attribute_management")
        perm_list.append("product_attribute_management")
        group.permissions.add(permission)
    if request.POST.get("perm6") == "true":
        permission = Permission.objects.get(codename="user_right_management_user")
        perm_list.append("user_right_management_user")
        group.permissions.add(permission)
    if request.POST.get("perm7") == "true":
        permission = Permission.objects.get(codename="user_right_management_role")
        perm_list.append("user_right_management_role")
        group.permissions.add(permission)
    group = Group.objects.get(name=group_name)
    groupCom = GroupCom()
    groupCom.id = int(group.id)
    groupCom.comStr = "0"
    groupCom.save()
    group_dic = {"id": group.id, "name": group.name, "perm_list": perm_list, "status":0}
    return JsonResponse(group_dic)


@login_required
@permission_required('webapp.user_right_management_role')
def modify_role(request):
    group_name = request.POST.get("group_name").strip()
    groupCount = Group.objects.filter(name=group_name).count()
    if groupCount > 1:
        return JsonResponse({"status": -1})
    group_id = request.POST.get("group_id")
    group = Group.objects.get(id=group_id)
    group.name = group_name
    group.permissions.clear()
    group.save()
    perm_list = []
    if request.POST.get("perm1") == "true":
        permission = Permission.objects.get(codename="product_information_inquiry")
        perm_list.append("product_information_inquiry")
        group.permissions.add(permission)
    if request.POST.get("perm2") == "true":
        permission = Permission.objects.get(codename="product_information_manage_new")
        perm_list.append("product_information_manage_new")
        group.permissions.add(permission)
    if request.POST.get("perm3") == "true":
        permission = Permission.objects.get(codename="product_information_manage_update")
        perm_list.append("product_information_manage_update")
        group.permissions.add(permission)
    if request.POST.get("perm4") == "true":
        permission = Permission.objects.get(codename="product_information_manege_check")
        perm_list.append("product_information_manege_check")
        group.permissions.add(permission)
    if request.POST.get("perm5") == "true":
        permission = Permission.objects.get(codename="product_attribute_management")
        perm_list.append("product_attribute_management")
        group.permissions.add(permission)
    if request.POST.get("perm6") == "true":
        permission = Permission.objects.get(codename="user_right_management_user")
        perm_list.append("user_right_management_user")
        group.permissions.add(permission)
    if request.POST.get("perm7") == "true":
        permission = Permission.objects.get(codename="user_right_management_role")
        perm_list.append("user_right_management_role")
        group.permissions.add(permission)
    group_dic = {"id": group_id, "name": group.name, "perm_list": perm_list,"status": 0}
    return JsonResponse(group_dic)


def delete_role(request):
    delete_id = request.GET.get("id")
    group = Group.objects.get(id=delete_id)
    group.permissions.clear()
    user_set = UserProfile.objects.filter(groups__id=delete_id)
    group_temp = Group.objects.get(name="无权限角色")
    if user_set.count() != 0:
        for user in user_set:
            user.groups.remove(group)
            user.groups.add(group_temp)
    group.delete()
    groupCom = GroupCom.objects.get(id=int(delete_id))
    groupCom.delete()
    return JsonResponse({"status": 0})


def user_check(request):
    username = request.GET.get("username")
    userCount = UserProfile.objects.filter(username=username.strip()).count()
    if userCount !=0:
        return JsonResponse({"status": -1})
    else:
        return JsonResponse({"status": 0})


@csrf_exempt
def send_group_company(request):
    gid = request.POST.get("id")
    strlist = json.loads(request.POST.get("list"))
    stri = ""
    for i in strlist:
        stri = i+stri
    groupCom = GroupCom.objects.get(id=int(gid))
    groupCom.comStr = stri
    groupCom.save()
    # return JsonResponse({"str": stri, "groupComStr": groupCom.comStr,"id":gid})
    return JsonResponse({"status": 0})


def get_group_company(request):
    gid = request.GET.get("id")
    groupCom = GroupCom.objects.get(id=int(gid))
    return JsonResponse({"comStr": groupCom.comStr})