import json
import logging

import os
from django.conf import settings
from django.http import JsonResponse , HttpResponse
from django.shortcuts import render
from wxcloudrun.models import Counters


logger = logging.getLogger('log')


def index(request, _):
    """
    获取主页

     `` request `` 请求对象
    """
    return HttpResponse('LE4T696JBL6vLmly'.encode('utf-8'))
"""
    return render(request, 'index.html')
"""

def trustdomain(request):
    # 定义 txt 文件的路径
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'WW_verify_LE4T696JBL6vLmly.txt')
    try:
        # 打开文件以二进制模式读取
        with open(file_path, 'rb') as file:
            # 创建 HttpResponse 对象，并设置响应内容为文件内容
            response = HttpResponse(file.read(), content_type='text/plain')
            # 设置响应头，指定文件名，以便浏览器下载文件
            response['Content-Disposition'] = 'attachment; filename=WW_verify_LE4T696JBL6vLmly.txt'
            return response
    except FileNotFoundError:
        # 如果文件不存在，返回 404 错误
        return HttpResponse(status=404)

def counter(request, _):
    """
    获取当前计数

     `` request `` 请求对象
    """

    rsp = JsonResponse({'code': 0, 'errorMsg': ''}, json_dumps_params={'ensure_ascii': False})
    if request.method == 'GET' or request.method == 'get':
        rsp = get_count()
    elif request.method == 'POST' or request.method == 'post':
        rsp = update_count(request)
    else:
        rsp = JsonResponse({'code': -1, 'errorMsg': '请求方式错误'},
                            json_dumps_params={'ensure_ascii': False})
    logger.info('response result: {}'.format(rsp.content.decode('utf-8')))
    return rsp


def get_count():
    """
    获取当前计数
    """

    try:
        data = Counters.objects.get(id=1)
    except Counters.DoesNotExist:
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    return JsonResponse({'code': 0, 'data': data.count},
                        json_dumps_params={'ensure_ascii': False})


def update_count(request):
    """
    更新计数，自增或者清零

    `` request `` 请求对象
    """

    logger.info('update_count req: {}'.format(request.body))

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if 'action' not in body:
        return JsonResponse({'code': -1, 'errorMsg': '缺少action参数'},
                            json_dumps_params={'ensure_ascii': False})

    if body['action'] == 'inc':
        try:
            data = Counters.objects.get(id=1)
        except Counters.DoesNotExist:
            data = Counters()
        data.id = 1
        data.count += 1
        data.save()
        return JsonResponse({'code': 0, "data": data.count},
                    json_dumps_params={'ensure_ascii': False})
    elif body['action'] == 'clear':
        try:
            data = Counters.objects.get(id=1)
            data.delete()
        except Counters.DoesNotExist:
            logger.info('record not exist')
        return JsonResponse({'code': 0, 'data': 0},
                    json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'code': -1, 'errorMsg': 'action参数错误'},
                    json_dumps_params={'ensure_ascii': False})
