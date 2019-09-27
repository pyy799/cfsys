import os
import xlrd
from webapp.models import Attribute
from webapp.shortcuts.ajax import ajax_success


def import_attribute():

    #录入属性数据库
    file = os.path.join('D:\Rong\PycharmProjects\cfsys\webapp\static', '属性.xlsx')
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name("属性")
    nrows = sheet.nrows

    for i in range(1, nrows):
        row = sheet.row_values(i)
      #  attribute_aid = row[0].strip()
        attribute_act = row[1].strip()
        attribute_attribute=row[2].strip()

        attribute_first_class=row[3].strip()
        if attribute_first_class == 'N.A.':
            attribute_first_class = None
        attribute_second_class=row[4].strip()
        if attribute_second_class == 'N.A.':
            attribute_second_class = None
        attribute_meaning=row[5].strip()
        attribute_info=row[6].strip()
        if attribute_info == 'N.A.':
            attribute_info = None

        attribute = Attribute()
        attribute.save()
       # attribute.attribute_id=attribute_aid
        attribute.ACT=attribute_act
        attribute.attribute=attribute_attribute
        attribute.first_class=attribute_first_class
        attribute.second_class=attribute_second_class
        attribute.meaning=attribute_meaning
        attribute.information=attribute_info

        attribute.save()
    # '属性id', '属性类型', '属性', '大类', '小类', '含义', '备注'


