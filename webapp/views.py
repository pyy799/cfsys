from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from webapp.shortcuts.ajax import ajax_success, ajax_error
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from webapp.upattribute import import_attribute
from webapp.models import Group,UserProfile,FindPassWord # GroupCom
import string
import random
import time
import base64
import hmac
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template import loader
from cfsys.settings import EMAIL_HOST_USER
import threading
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

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
                # 以下是为了获取该用户对应的关联公司
                # username = request.POST.get("username")
                # user = UserProfile.objects.get(username=username)
                # gr = Group.objects.get(user=user)
                # comstr = GroupCom.objects.get(id=gr.id).comStr
                # ucompany = str(user.uCompany)
                # if "0" in comstr:
                #     if ucompany in comstr:
                #         comstr = comstr.replace("0", "")
                #     else:
                #         comstr = comstr.replace("0", ucompany)
                # request.session["relate_company"] = comstr
                return ajax_success()
            else:
                return ajax_error("dsf")
        except:
            return ajax_error("dsf")


@login_required
def logout_func(request):
    logout(request)
    return HttpResponse('欢迎下次光临!')


def findpassword(request):
    return render(request,"findpassword.html")


def start_findpassword(request):
    username = request.POST.get("username")
    user_set = UserProfile.objects.filter(username=username)
    if not user_set.exists():
        return JsonResponse({"status":-1})
    user = UserProfile.objects.get(username=username)
    return JsonResponse({"status": 0, "email": user.email,"username":user.username})


from cfsys.settings import EMAIL_FROM
def check_email(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    key = generate_key()
    token = generate_token(key)
    findpd = FindPassWord()
    findpd.username = username
    findpd.key = key
    findpd.token = token
    findpd.email = email
    findpd.save()
    fid = FindPassWord.objects.get(token=token).id
    urlString = "http://localhost:8000/reset_password?id="+str(fid)+"&token="+str(token,"utf-8")
    html_content = loader.render_to_string("email_template.html",{"username":username,"urlString":urlString})
    # send_html_email(subject="长峰产品管理系统",html_content=html_content,recipient_list=[email])
    send_email("长峰产品管理系统", html_content, EMAIL_FROM,[email], False,"text/html")
    return JsonResponse({"status": 0})


def reset_password(request):
    fid = request.GET.get("id")
    token = request.GET.get("token").encode("utf-8")
    count = FindPassWord.objects.filter(id=int(fid)).count()
    if count == 0:
        return HttpResponse("token已过期,重置密码失败!")
    findpassword = FindPassWord.objects.get(id=int(fid))
    ikey = findpassword.key
    if not check_token(ikey,token):
        return HttpResponse("token已过期,重置密码失败!")
    username = findpassword.username
    return render(request,"resetpassword.html",{"username":username})


@csrf_exempt
def reset_password_success(request):
    password = request.POST.get("password")
    username = request.POST.get("username")
    print(password)
    print(username)
    count = UserProfile.objects.filter(username=username)
    if count == 0:
        return HttpResponse("修改密码失败!")
    else:
        user = UserProfile.objects.get(username=username)
        user.set_password(password)
        user.save()
        return HttpResponseRedirect("/login/")

# 生成key


def generate_key():
    str_from = string.ascii_letters + string.digits
    count = 8
    key = []
    for i in range(count):
        s = random.choice(str_from)
        key.append(s)
    return "".join(key)


# 生成token
def generate_token(key, expire=1800):
    # key为用户指定的key,expire为过期时间,单位为秒
    ts_str = str(time.time()+expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, "sha1").hexdigest()
    token = ts_str + ':'+sha1_tshexstr
    bs64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return bs64_token


# 验证token
def check_token(key,token):
    token_str = base64.urlsafe_b64decode(token).decode("utf-8")
    token_list = token_str.split(':')
    if len(token_list)!=2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        return False
    known_sha1_ts_str = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode("utf-8"),'sha1').hexdigest()
    if sha1 != known_sha1_ts_str:
        return False
    return True


def send_html_email(subject,html_content,recipient_list):
    msg = EmailMessage(subject,html_content,EMAIL_HOST_USER,recipient_list)
    msg.content_subtype = "html"
    msg.send()


class EmailThread(threading.Thread):
    def __init__(self,subject,body,from_email,recipient_list,fail_silently,html):
        self.subject = subject
        self.body = body
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject,self.body,self.from_email,self.fail_silently,self.recipient_list)
        if self.html:
            msg.attach_alternative(self.body,self.html)
        msg.send(self.fail_silently)


def send_email(subject, body, from_email, recipient_list, fail_silently=False, html=None):
    EmailThread(subject, body, from_email, recipient_list, fail_silently,html).start()


@login_required
def userinformation(request):
    print(request.user.username)
    user = UserProfile.objects.get(username=request.user.username)
    company = user.get_company(user.uCompany)
    role = Group.objects.get(user=user)
    rolename = role.name
    res = {
        "username": request.user.username,
        "gender": user.gender,
        "phone":user.phone,
        "email": user.email,
        "company": company,
        "department": user.department,
        "position": user.position,
        "role": rolename
    }
    return render(request, "userinformation.html", res)


@login_required
def ones_modify(request):
    username = request.POST.get("username")
    dtype = request.POST.get("type")
    user = UserProfile.objects.get(username=username)
    if dtype == "1":
        phone = request.POST.get("phone")
        user.phone = phone
    else:
        email = request.POST.get("email")
        user.email = email
    user.save()
    return JsonResponse({"status": 0})


@login_required
def check_pd(request):
    username = request.POST.get("username")
    pd = request.POST.get("pd")
    user = authenticate(username=username, password=pd)
    if user is not None:
        return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": -1})


@login_required
def new_pd(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = UserProfile.objects.get(username=username)
    if user is None:
        return JsonResponse({"status": -1})
    else:
        user.set_password(password)
        user.save()
        return JsonResponse({"status": 0})