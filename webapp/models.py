from django.db import models
from django.contrib.auth.models import User, Group
from webapp.const import *


# 角色
class Role(Group):
    roleName = models.CharField("角色名称", max_length=32, blank=False, null=False)
    pSearch = models.BooleanField("产品信息查询权限", default=False)
    pInfoNew = models.BooleanField("产品信息管理_新建", default=False)
    pInfoUpdate = models.BooleanField("产品信息管理_更新", default=False)
    pInfoCheck = models.BooleanField("产品信息管理_审核", default=False)
    pAttritube = models.BooleanField("产品属性管理", default=False)
    userManagement = models.BooleanField("用户权限管理_用户", default=False)
    roleManagement = models.BooleanField("用户权限管理_角色", default=False)

    def __str__(self):
        return self.roleName


COMPANY_CHOICE = (
    (Company.GU_FEN, "股份"),
    (Company.JING_YI, "精一"),
    (Company.KE_WEI, "科威"),
    (Company.YI_LIAO, "医疗"),
    (Company.BO_KE, " 柏克"),
    (Company.KE_JI, "科技"),
    (Company.ZHE_ZI, "浙子")
)


# 用户
class UserProfile(User):
    userName = models.CharField("中文名", max_length=32, blank=False, null=False, default="")
    userPassword = models.CharField("密码", max_length=32, blank=False, null=False, default="123456")
    uCompany = models.IntegerField("公司", blank=True, null=True, choices=COMPANY_CHOICE)
    department = models.CharField("部门", max_length=32, blank=True, null=True)
    userRole = models.ForeignKey(Role, verbose_name="用户角色", related_name="user_role",
                                 default=1, blank=True, null=False)
    isValid = models.BooleanField("是否有效", default=True, blank=False, null=False)


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


STATUS_CHOICE = (
    (ProductStatus.WAIT_SUBMIT, "待提交"),
    (ProductStatus.WAIT_PASS, "待审核"),
    (ProductStatus.PASS, "审核通过"),
    (ProductStatus.FAIL, "审核不通过"),
    )


# 产品
class Product(models.Model):
    productNum = models.CharField("产品编号", max_length=32, blank=False, null=False)
    productName = models.CharField("产品名称", max_length=64, blank=False, null=False)
    pCompany = models.IntegerField("公司", blank=True, null=True, choices=COMPANY_CHOICE)
    department = models.CharField("部门", max_length=32, blank=True, null=True)
    uploader = models.ForeignKey(UserProfile, verbose_name="上传者", related_name="uploader", blank=True, null=True)
    upload_time = models.DateField("审核通过日期", null=True, blank=True)
    introduction = models.CharField("产品介绍", max_length=1024, blank=True, null=True)

    maturity = models.ForeignKey(Attribute, verbose_name="成熟度", related_name="maturity", blank=True, null=True)
    independence = models.ForeignKey(Attribute, verbose_name="自主程度", related_name="independence", blank=True, null=True)
    business = models.ForeignKey(Attribute, verbose_name="业务领域", related_name="business", blank=True, null=True)
    technology = models.ForeignKey(Attribute, verbose_name="技术形态", related_name="technology", blank=True, null=True)

    attribute_num = models.CharField("属性编号", max_length=32, blank=True, null=True)
    status = models.IntegerField("产品状态", choices=STATUS_CHOICE, default=ProductStatus.WAIT_SUBMIT)
    reason = models.CharField("不通过原因", max_length=1024, blank=True, null=True)
    fileName = models.CharField("审核文件", max_length=64, blank=True, null=True)
    isVaild = models.BooleanField("是否有效", default=True, blank=False, null=False)









