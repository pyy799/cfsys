# coding: utf-8

import traceback
import datetime
import logging
import os
from cfsys.settings import LOGGING_DEBUG, LOGGING_PATH

_INFO = 'info'
_DEBUG = 'debug'
_ERROR = 'error'


def _get_path(log_type):
    """
    获取记录日志的路径
    """
    if not os.path.exists(LOGGING_PATH):
        os.makedirs(LOGGING_PATH)

    date = datetime.datetime.today().strftime('%Y-%m-%d')

    path = {
        _INFO: os.path.join(LOGGING_PATH, date + '.info.log'),
        _DEBUG: os.path.join(LOGGING_PATH, date + '.debug.log'),
        _ERROR: os.path.join(LOGGING_PATH, date + '.error.log'),
    }[log_type]

    return path


def _log_handle(log_type):
    """
    获取logging handle
    @params log_type: 日志类型，字符串类型，可选项：'info', 'debug', 'error'。
    """
    _path = _get_path(log_type)

    log_name, path, level, template = {
        _INFO: (
            'INF', _path, logging.INFO,
            '[%(asctime)s %(levelname)3s]\n%(message)s\n'
        ),
        _DEBUG: (
            'DBG', _path, logging.DEBUG,
            '[%(asctime)s %(levelname)3s %(pathname)s]\n'
            '[%(module)s.%(funcName)s]\n%(message)s\n'
        ),
        _ERROR: (
            'ERR', _path, logging.WARNING,
            '[%(asctime)s %(levelname)3s %(pathname)s]\n'
            '[%(module)s.%(funcName)s in line %(lineno)d %(threadName)s]\n%(message)s\n'
        )
    }[log_type]

    _logger = logging.getLogger(log_name)
    _formatter = logging.Formatter(template)

    # 输出到文件
    _f_hdlr = logging.FileHandler(path)
    _f_hdlr.setFormatter(_formatter)
    _logger.addHandler(_f_hdlr)

    # 输出到屏幕
    _c_hdlr = logging.StreamHandler()
    _c_hdlr.setFormatter(_formatter)
    _logger.addHandler(_c_hdlr)

    _logger.setLevel(level)
    return _logger


log_info = _log_handle(_INFO).info if LOGGING_DEBUG else lambda x: ''
log_debug = _log_handle(_DEBUG).debug if LOGGING_DEBUG else lambda x: ''
log_error = _log_handle(_ERROR).error if LOGGING_DEBUG else lambda x: ''


def error_traceback():
    """
    记录错误的具体原因
    """
    error_logging = _get_path(_ERROR)
    if os.path.exists(error_logging):
        f = open(error_logging, "w")
        traceback.print_exc(file=f)
        f.close()
    else:
        traceback.print_exc()
