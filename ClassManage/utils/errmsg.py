# -*- coding:utf-8 -*-
# 0为操作成功
SUCCESS = {'code': 0}

# 1 - 100 与请求参数相关
PARAMETER_TYPE_ERROR = {'code': 1, 'message': '参数类型错误'}
PARAMETER_ERROR = {'code': 2, 'message': '请求参数有误'}
INCOMPLETE_PARAMETERS = {'code': 3, 'message': '请求参数不完整'}

# 101 - 200 与数据库相关
DATA_SAVE_ERROR = {'code': 101, 'message': '数据保存异常'}
NO_SUCH_DATA = {'code': 102, 'message': '没有相关数据'}