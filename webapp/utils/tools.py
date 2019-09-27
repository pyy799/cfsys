# # coding: utf-8
#
# import binascii
# import calendar
# import datetime
# import hashlib
# import json
# import math
# import time
# import urllib.parse
# import urllib.request
# from Crypto.Cipher import DES
# from webapp import log
#
#
# class THQS:
#     required_args = ('time', 'hash')
#
#     @classmethod
#     def encode(cls, salt_key, params, rtime=None, only_hash=False):
#         """加密"""
#         kv_pairs = list()
#         for k, v in params.items():
#             k = urllib.parse.quote_plus(str(k))
#             v = urllib.parse.quote_plus(str(v))
#             url_param = "%s=%s" % (k, v)
#             kv_pairs.append(url_param)
#
#         kv_pairs.sort()
#         prefix = "&".join(kv_pairs)
#         rtime = rtime if rtime else int(time.time())
#
#         url_args = "&".join((prefix, "time=%s" % rtime, "salt=%s" % salt_key))
#
#         hash_value = hashlib.new('md5', url_args.encode('utf8')).hexdigest().upper()
#         if only_hash:
#             return hash_value
#
#         hash_pairs = "hash=%s" % hash_value
#         return "&".join((prefix, 'time=%s' % rtime, hash_pairs))
#
#     @classmethod
#     def is_matched(cls, salt_key, params):
#         """解密"""
#         for key in cls.required_args:
#             if key not in params:
#                 log.log_error("[THQS] 缺少参数")
#                 return False
#
#         temp = {}
#         for key, value in params.items():
#             temp[key] = urllib.parse.quote_plus(str(value), safe="~()*!.\'")
#
#         params = temp
#
#         ptime = int(params.get('time'))
#         # 如果对方发送请求的时间戳是以毫秒为单位，时间参数是13位。否则是10位。
#         if len(str(ptime)) == 13:
#             ptime = int(ptime) / 1000
#
#         duration = int(time.time()) - ptime
#         if abs(duration) > 300:
#             log.log_error("[THQS] 时间超过5分钟，THQS过期")
#             return False
#
#         kv_pairs = ["%s=%s" % (key, value) for key, value in params.items() if key not in ('hash', 'time')]
#         kv_pairs.sort()
#
#         temp_string = "&".join(kv_pairs)
#         prefix = "&".join((temp_string, "time=%s" % params.get('time'), 'salt=%s' % salt_key))
#         hash_md5 = hashlib.new('md5', prefix.encode('utf8')).hexdigest().upper()
#
#         if params.get('hash', '') != hash_md5:
#             log.log_error("[THQS] hash参数不正确")
#             return False
#
#         return True
#
#
# def request_api(url, params, key=None, cdn=False):
#     """
#     根据thqs加密规则，请求json内容
#     :param url: 请求链接
#     :param params: 请求参数
#     :param key: 请求加密key（cdn不需要thqs方式）
#     :return: 请求的json结果
#     """
#     if not cdn:
#         if not key:
#             log.log_error("缺少THQS_KEY")
#             return None
#         else:
#             qurl = "?".join([url.rstrip("?"), THQS().encode(key, params)])
#     else:
#         qurl = url % params
#
#     try:
#         with urllib.request.urlopen(qurl, timeout=60) as fd:
#             data = json.loads(fd.read().decode('utf8'))
#         log.log_info("[Get Data]: %s\n%s" % (qurl, data))
#         return data
#     except Exception as e:
#         log.log_error("[Request Error]: %s\n%s" % (qurl, e))
#         log.error_traceback()
#         return None
#
#
#
# def time_it(func):
#     """
#     计算函数消耗时间（装饰器）
#     """
#
#     def _deco(*args, **kwargs):
#         start = datetime.datetime.now()
#         print("--- Start time: %s ---" % start)
#         ret = func(*args, **kwargs)
#         end = datetime.datetime.now()
#         print("---- End time: %s ----" % end)
#         print("Function spend time: %s" % (end - start))
#         return ret
#
#     return _deco
#
#
#
# def month_range(month):
#     """
#     某个月的范围
#     """
#     y, m = [int(i) for i in month.split("-")]
#     _start = datetime.date(y, m, 1)
#     _end = datetime.date(y, m, calendar.monthrange(y, m)[-1])
#     return _start, _end
#
#
# def get_dates(start, end):
#     """
#     获得指定日期内所以日期列表
#     """
#     if start > end:
#         return ()
#
#     d = start
#     while d <= end:
#         yield d
#         d += datetime.timedelta(days=1)
#
#
# def get_months(start, end, mtype="date"):
#     """
#     获得月份列表（从start到end）
#     """
#     if start > end:
#         return ()
#
#     if mtype not in ["str", "date"]:
#         raise TypeError
#
#     tm = start
#     while tm <= end:
#         if isinstance(start, datetime.date) and isinstance(end, datetime.date):
#             if mtype == "date":
#                 yield tm
#             else:
#                 yield tm.strftime("%Y-%m")
#
#             tm = next_month(tm, mtype="date")
#         else:
#             if mtype == "date":
#                 y, m = [int(i) for i in tm.split("-")]
#                 tm = datetime.date(y, m, 1)
#
#             yield tm
#             tm = next_month(tm)
#
#
# def months_number(start, end):
#     """
#     从start到end总共有多少个月
#     """
#     month = len([m for m in get_months(start, end)])
#     if end.day <= start.day:
#         month -= 1
#
#     return month or 1  # 同一个月之内，month有可能为0，为0的时候返回1
#
#
# def calc_days(date):
#     """
#     计算本月到今天的天数和本月的最大天数
#     """
#     y, m, d = date.year, date.month, date.day
#     _, mdays = calendar.monthrange(y, m)
#     return d, mdays
#
#
# def scale_transform(num, unit_from="B", unit_to="G", scale=1024):
#     """
#     进制转换
#     """
#     try:
#         num = float(num)
#     except Exception as e:
#         print("Param \"%s\" is not a number.\n%s", (num, e))
#         return None
#     uni_unit_dict = {"B": "B", "b": "B",
#                      "K": "K", "k": "K", "KB": "K", "kb": "K",
#                      "M": "M", "m": "M", "MB": "M", "mb": "M",
#                      "G": "G", "g": "G", "GB": "G", "gb": "G",
#                      "T": "T", "t": "T", "TB": "T", "tb": "T",
#                      }
#
#     unit_from = uni_unit_dict.get(unit_from)
#     unit_to = uni_unit_dict.get(unit_to)
#
#     if not unit_from or not unit_to:
#         print("Can't recognize this unit.")
#         return None
#
#     unit_list = ["B", "K", "M", "G", "T"]
#     amount_list = [math.pow(scale, i) for i in range(len(unit_list))]
#
#     return num * amount_list[unit_list.index(unit_from)] / amount_list[(unit_list.index(unit_to))]
#
#
# def make_html_table(functions, moneys=None, edit=True):
#     """
#     把基础模块做成一个html table
#     """
#     if functions.count() == 0:
#         return ""
#
#     func_list = [[f.level1name, f.level2name, f.content] for f in functions]
#     func_first = func_list[0]
#
#     tr_num_list = [[[i, 1] for i in func_first]]
#     last_name = [[i, 0] for i in func_first]
#
#     for i, func in enumerate(func_list):
#         if i == 0:
#             continue
#
#         new_line = []
#         for lv, f in enumerate(func):
#             if f == last_name[lv][0]:
#                 count = int(last_name[lv][1])
#                 tr_num_list[count][lv][1] += 1
#                 new_line.append([])
#             else:
#                 new_line.append([f, 1])
#                 last_name[lv] = [f, i]
#
#         tr_num_list.append(new_line)
#
#     if not moneys:
#         moneys = {0: (len(func_list), 0)}
#
#     tr_list = []
#     for i, td_line in enumerate(tr_num_list):
#         tr = '<tr>'
#         for j in td_line:
#             if not j:
#                 continue
#             if edit:
#                 tr += '<td rowspan="%d">%s</td>' % (j[1], j[0]) if j[1] > 1 else \
#                     '<td><input type="checkbox" class="pull-left check" name="checked" value="%d"> %s</td>' % (i+1, j[0])
#             else:
#                 tr += '<td rowspan="%d">%s</td>' % (j[1], j[0]) if j[1] > 1 else \
#                     '<td>%s</td>' % (j[0])
#
#         rows, money = moneys.get(i, (0, 0))
#         if rows:
#             if edit:
#                 tr += '<td rowspan="%d" id="money%d"><input value="%d" name="money"></td>' % (rows, i, money)
#             else:
#                 tr += '<td rowspan="%d" id="money%d">%d</td>' % (rows, i, money)
#
#         tr += '</tr>'
#         tr_list.append(tr)
#
#     return "".join(tr_list)
#
#
# def get_function_table(contract):
#     """
#     获得全部服务的基础功能列表，组成页面table html
#     """
#     def _get_table(stype):
#         """获得某一种服务的基础功能列表，组成页面table html"""
#         from webapp.models import BasicModule
#
#         if stype not in ["video", "live", "liveclass"]:
#             return ""
#
#         _func_list = json.loads(getattr(contract, "basic_function_%s" % stype))
#
#         if _func_list:
#             _id_list = []
#             for _dict in _func_list:
#                 _id_list += _dict.get("function")
#
#             _basic_function = BasicModule.objects.filter(pk__in=_id_list)
#
#             _moneys = {}
#             _line = 0
#             for _dict in _func_list:
#                 if _dict.get("function"):
#                     _moneys[_line] = [len(_dict.get("function")), _dict.get("money")]
#                     _line += len(_dict.get("function"))
#
#             _table = make_html_table(_basic_function, _moneys, False)
#         else:
#             _table = ""
#
#         return _table
#
#     return {"table_%s" % i: _get_table(i) for i in ["video", "live", "liveclass"]}
