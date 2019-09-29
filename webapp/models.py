import datetime
from django.db import models
from django.contrib.auth.models import User, Group
from webapp.const import *


COMPANY_CHOICE = (
    (Company.GU_FEN, "股份"),
    (Company.JING_YI, "精一"),
    (Company.KE_WEI, "科威"),
    (Company.YI_LIAO, "医疗"),
    (Company.BO_KE, " 柏克"),
    (Company.KE_JI, "科技"),
    (Company.ZHE_ZI, "浙子")
)


class UserProfileManager(models.Manager):
    def create_user(self, username, password, gender,
                    uCompany,department, position,role, phone,
                    email, is_active=True):
        user = self.model()
        user.username = username
        user.set_password(password)
        user.gender = gender
        user.uCompany = uCompany
        user.department = department
        user.position = position
        user.phone = phone
        user.email = email
        user.is_active = is_active
        group = Group.objects.get(pk=role)
        user.save()
        user.groups.add(group)


class UserProfile(User):
    objects2 = UserProfileManager()
    gender = models.IntegerField("性别", blank=False, null=False)
    uCompany = models.IntegerField("公司", choices=COMPANY_CHOICE, blank=True, null=True)
    department = models.CharField("部门", max_length=32, blank=True, null=True)
    position = models.CharField("职位", max_length=32, blank=True, null=True)
    phone = models.CharField("电话", max_length=32, blank=True, null=True)

    def get_company(self, com):
        """获取用户公司名称 """
        return dict(COMPANY_CHOICE).get(com)

    class Meta:
        permissions = [
            ('user_right_management_user','用户权限管理_用户'),
            ('user_right_management_role','用户权限管理_角色'),
        ]
        default_permissions = []
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userName


ACT_CHOICE = (
    (AttributeType.A, "属性"),
    (AttributeType.C, "属性大类"),
    (AttributeType.T, "属性小类"),
)


class Attribute(models.Model):
    ACT = models.CharField("类型", max_length=32, blank=False, null=False, choices=ACT_CHOICE)
    attribute = models.CharField("属性缩写", max_length=32, blank=False, null=False)
    first_class = models.CharField("大类缩写", max_length=32, blank=True, null=True)
    second_class = models.CharField("小类缩写", max_length=32, blank=True, null=True)
    meaning = models.CharField("含义", max_length=32, blank=True, null=True)
    information = models.CharField("备注", max_length=1024, blank=True, null=True)

    class Meta:
        permissions = [
            ('product_attribute_management','产品属性管理'),
        ]
        default_permissions = []


STATUS_CHOICE = (
    (ProductStatus.WAIT_SUBMIT, "待提交"),
    (ProductStatus.WAIT_PASS, "待审核"),
    (ProductStatus.PASS, "审核通过"),
    (ProductStatus.FAIL, "审核不通过"),
    )

APPLY_CHOICE = (
    (ApplyStatus.NEW, "新建"),
    (ApplyStatus.ALTER, "修改"),
    (ApplyStatus.DELETE, "删除"),
    (ApplyStatus.INVALID, "停用"),
)


# 产品
class Product(models.Model):
    product_num = models.CharField("产品编号", max_length=32, blank=False, null=False)
    product_name = models.CharField("产品名称", max_length=64, blank=False, null=False, default="")
    old_product_name = models.CharField("旧产品名称", max_length=64, blank=True, null=True)

    introduction = models.CharField("产品描述", max_length=1024, blank=True, null=True)
    is_overlap = models.BooleanField("是否重叠", blank=True, null=False,default=False)
    target_field = models.CharField("目标行业", max_length=1024, blank=True, null=True)
    apply_situation = models.CharField("应用场景", max_length=1024, blank=True, null=True)
    example = models.CharField("市场案例", max_length=1024, blank=True, null=True)
    one_year_money = models.FloatField("过去一年销售额", default=0)
    one_year_num = models.IntegerField("过去一年销售数量", default=0)
    three_year_money = models.FloatField("过去三年销售额", default=0)
    three_year_num = models.IntegerField("过去三年销售数量", default=0)
    pCompany = models.IntegerField("所属公司", blank=True, null=True, choices=COMPANY_CHOICE)
    contact_people = models.CharField("联系人", max_length=64, blank=True, null=True)
    remark = models.CharField("备注", max_length=1024, blank=True, null=True)
    uploader = models.ForeignKey(UserProfile, verbose_name="上传者", related_name="uploader", blank=True, null=True)

    upload_time = models.DateField("提交时间", null=True, blank=True)
    pass_time = models.DateField("发布时间", null=True, blank=True)

    real_name = models.CharField("文件原名", max_length=64, blank=True, null=True, default="")
    save_name = models.CharField("文件原名", max_length=64, blank=True, null=True, default="")

    maturity = models.ForeignKey(Attribute, verbose_name="成熟度", related_name="maturity", blank=True, null=True)
    independence = models.ForeignKey(Attribute, verbose_name="自主度", related_name="independence", blank=True, null=True)
    business = models.ForeignKey(Attribute, verbose_name="业务领域", related_name="business", blank=True, null=True)
    technology = models.ForeignKey(Attribute, verbose_name="技术形态", related_name="technology", blank=True, null=True)

    attribute_num = models.CharField("属性编号", max_length=32, blank=True, null=True)
    status = models.IntegerField("审批状态", choices=STATUS_CHOICE, default=ProductStatus.WAIT_SUBMIT)
    apply_type = models.IntegerField("申请类型", choices=APPLY_CHOICE, default=ApplyStatus.NEW)
    reason = models.CharField("不通过原因", max_length=1024, blank=True, null=True)
    version = models.IntegerField("产品版本", default=1)
    is_vaild = models.BooleanField("是否有效", default=True, blank=False, null=False)

    def company_name(self, cnum):
        """公司名称"""
        return dict(COMPANY_CHOICE).get(cnum)

    def status_name(self, snum):
        """审批状态"""
        return dict(STATUS_CHOICE).get(snum)

    def apply_name(self, anum):
        """申请类型"""
        return dict(APPLY_CHOICE).get(anum)

    def pack_data(self):
        """
        数据打包
        """
        def get_value(s, field):
            if isinstance(getattr(self, field.name), datetime.date):
                return getattr(self, field.name).strftime("%Y-%m-%d")
            elif field.name in ["maturity", "independence", "business", "technology"]:
                return getattr(getattr(self, field.name), "meaning", '')
            elif field.name == "uploader":
                return getattr(getattr(self, field.name), "userName", '')
            return getattr(s, field.name) or ''

        data = []
        [data.append((f.name, get_value(self, f) or '')) for f in self._meta.fields]

        data.append(("is_overlap", "是" if self.is_overlap else "否"))
        data.append(("pCompany_name", self.company_name(self.pCompany)))
        data.append(("status_name", self.status_name(self.status)))
        data.append(("apply_type_name", self.apply_name(self.apply_type)))
        data.append(("is_vaild", "是" if self.is_vaild else "否"))

        return dict(data)

    class Meta:
        permissions = [
            ('product_information_inquiry','产品信息查询'),
            ('product_information_manage_new','产品信息管理_新建'),
            ('product_information_manage_update','产品信息管理_更新'),
            ('product_information_manege_check','产品信息管理_审核')
        ]
        default_permissions = []

