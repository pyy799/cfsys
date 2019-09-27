# coding: utf-8

import json
from cfsys import settings
# from webapp.utils.tools import request_api


# region # 数据库查询 #

def get_query(request, model, order=None, **fil):
    """
    分区间请求数据， 解决数据过大造成请求慢的问题
    :param request：为前端post请求参数集合，主要用到start, length参数
    :param start：获取区间的起始位置
    :param length：区间长度
    :param fil：过滤的参数集合, 类型dict
    :returns: data: django query_set 集合；count: 数据总量；是否成功
    """
    try:
        start = int(request.POST.get("start", 0))
        length = int(request.POST.get("length", 0))
    except ValueError:
        return [], 0, False

    if not length:
        return [], 0, False

    if fil:
        data = model.objects.filter(**fil)
    else:
        data = model.objects.all()

    # datatable 封装的过滤功能
    if request.POST.get("action") and request.POST.get("action") == "filter":
        filter_params = json.loads(request.POST.get("filter"))
        new_filter_params = {k: v for k, v in filter_params.items() if v}
        if new_filter_params:
            data = data.filter(**new_filter_params)

    if order:
        data = data.order_by(*order)

    count = len(data)
    data = data[start: start + length]

    return data, count, True


def get_advanced_query(request, model, order=None, excepts=None):
    if not excepts:
        excepts = []

    if request.POST.get("action") and request.POST.get("action") == "filter":
        filter_params = json.loads(request.POST.get("filter"))
        new_filter_params = {k: v for k, v in filter_params.items() if filter_params[k] and k not in excepts}

        data = model.objects.filter(**new_filter_params)
    else:
        data = model.objects.all()

    if order:
        data = data.order_by(*order)

    return data


def create_data(draw, data, total):
    """
    拼装datatable需要的返回数据格式
    draw: datatable参数
    data: 需要返回的数据集合
    total: 数据的总条数
    """
    return json.dumps({"draw": draw, "data": data, "recordsFiltered": total, "recordsTotal": total})

# endregion

