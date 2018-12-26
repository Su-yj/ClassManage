import json


def parse_json(request):
	"""
    解析json数据
    :param request: 请求内容
    :return: data, 请求参数
    """
	try:
		json_data = json.loads(request.body.decode())
		return json_data
	except:
		return None
