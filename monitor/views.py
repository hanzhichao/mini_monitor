# coding:utf-8
import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from monitor.serializers import AppSerializer, AppStatisticsSerializer
from monitor.serializers import AppHistorySerializer, GroupSerializer,HostSerializer
from monitor.models import App, AppStatistics, AppHistory, Group, Host
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from monitor.util.util import get_ip
from datetime import datetime
import json


@api_view(['GET', 'POST'])
@csrf_exempt
def app_list(request):
    """
    GET请求：列出所有app，或指定group下的app
    POST请求：创建一个app
    POST参数：name
    
    """
    if request.method == 'GET':
        group_id = request.GET.get('group_id', None)
        if group_id:
            tasks = App.objects.filter(enable=1).filter(group_id=group_id).all()
        else:
            tasks = App.objects.filter(enable=1).all()
        serializer = AppSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        name = request.data.get('name', None)
        # app = App.create(name, 1, "OK", "", 1, 2).save()   # 这样save()后返回值为null,拿不到对象
        app = App.create(name, 1, "OK", "", 1, 2)
        app.save()
        serializer = AppSerializer(app, many=False)
        logging.error(app)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def app_detail(request, pk):
    """
    Get,update or delete a specific app
    """
    try:
        try:
            pk = int(pk)
            app = App.objects.get(pk=pk)
        except App.DoesNotExist:
            app = App.objects.filter(name=pk).first()
    except App.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AppSerializer(app)
        return JsonResponse(serializer.data)

    if request.method == 'DELETE':
        serializer = AppSerializer(app)
        app.enable = 0
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        if not app:
            res = {"code":405,"message":"Not found this app"}
            return Response(data=res,status=405)

    ip = get_ip(request)
    if ip is not None:
        host = Host.objects.filter(ip=ip).first()
        if host is None:
            host = Host.create(ip)
            host.save()
    status = request.data.get("status")
    statistics = request.data.get("message", app.message)
    if status is None:
        res = {"code": 400, "message": "wong"}
        return Response(data=res, status=400)
    app.status = status
    app.last_update = datetime.now()
    app.host_id = host.id
    app.save()
    if statistics:
        try:
            json.loads(statistics)
        except:
            res = {"code":400,"message":"Statistics format must json"}
            return Response(data=res,status=400)
        appStatistics = AppStatistics.create(statistics,app.id)
        appStatistics.save()
        serializer = AppSerializer(app)
    return JsonResponse(serializer.data)


def manage_detail(request, pk):
    try:
        pk = int(pk)
        app = App.objects.get(pk=pk)
    except:
        app = App.objects.filter(name=pk).first()
    if not app:
        return HttpResponse(status=404)

    elif request.method == 'GET':
        serializer = manageAppSerializer(app)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        app.name = request.data.get("name", app_name)
        app.host_id = request.data.get("host_id", app.host_id)
        app.group_id = request.data.get("group_id", app.group_id)
        app.configuration = request.data.get("configuration", app.configuration)
        app.save()
        serializer = manager_app_serializer(app, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
@csrf_exempt
def app_statistics_list(request):
    """
    List all app_statisticss or create a new app statistics
    """
    if request.method == 'GET':
        tasks = AppStatistics.objects.all()
        serializer = AppStatisticsSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # serializer = AppStatisticsSerializer(data=request.DATA)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=201)
        app_id = request.data.get('app_id')
        statistics = request.data.get('statistics')
        descrstatisticstion = request.data.get('descrstatisticstion')
        if app_id and statistics:
            checkappid = AppStatistics.objects.filter(app_id=app_id).first()
            if checkappid:
                res = {"code":400,
                "message": "Ops! app id already exists"}
                return Response(data=res, status=400)
            
            checkstatistics = AppStatistics.objects.filter(statistics=statistics).first()
            if checkstatistics:
                res = {"code": 400, "message": "Ops! app statistics already exists"}
                return Response(data=res, status=400)
        else:
            res = {"code": 400, "message": "Ops!app statistics app id and statistics can't be null"}
            return Response(data=res, status=400)
        app_statistics = AppStatistics.create(app_id, statistics, description)
        app_statistics.save()
        serializer = AppStatisticsSerializer(app_statistics, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET','PUT','DELETE'])
def app_statistics_detail(request, pk):
    """
    Get,update or delete a specific app_statistics
    """
    try:
        app_statistics = app_statistics.objects.get(pk=pk)
    except app_statistics.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AppStatisticsSerializer(app_statistics)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        app_statistics.app_id = request.data.get('app_id',app_statistics.app_id)
        app_statistics.statistics = request.data.get('statistics',
            app_statistics.statistics)
        app_statistics.save()
        serializer = AppStatisticsSerializer(app_statistics)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        app_statistics.delete()
        res = {"code": 200, "message": "Delete Suessus!"}
        return Response(data=res, status=200)


@api_view(['GET', 'POST'])
@csrf_exempt
def app_history_list(request):
    """
    List all app_historys or create a new app_history
    """
    if request.method == 'GET':
        limit = request.GET.get('limit', 12)
        app_id = request.GET.get('app_id')
        try:
            limit = int(limit)
            app_id = int(app_id)
        except ValueError:
            res = {"code": 404, "message": "app_id and limit must be int"}
            return Response(data=res, status=400)

        history_list = AppHistory.objects.filter(app_id=app_id).order_by('-id')[:limit]
        serializer = AppHistorySerializer(history_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # serializer = app_historySerializer(data=request.DATA)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=201)
        app_id = request.data.get('app_id')
        status = request.data.get('status')
        message = request.data.get('message')
        if not app_id or not status:
            res = {"code": 400, "message": "Ops!app history app_id and status can't be null"}
            return Response(data=res, status=400)
        app_history = AppHistory.create(app_id, status, message)
        app_history.save()
        serializer = AppHistorySerializer(app_history, many=False)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def app_history_detail(request, pk):
    """
    Get,update or delete a specific app_history
    """
    try:
        app_history = AppHistory.objects.get(pk=pk)
    except AppHistory.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AppHistorySerializer(app_history)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        app_history.app_id = request.data.get('app_id', app_history.app_id)
        app_history.message = request.data.get('app_history')
        app_history.status = request.data.get('status', app_history.status)
        app_history.save()
        serializer = AppHistorySerializer(app_history)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        Host.delete()
        res = {"code": 200, "message": "Delete Suessus!"}
        return Response(data=res, status=200)


@api_view(['GET'])
@csrf_exempt
def group_list(request):
    """
    List all groups or create a new group
    """
    if request.method == 'GET':
        tasks = Group.objects.all()
        serializer = GroupSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    """
    Get,update or delete a specific group
    """
    try:
        group = Group.objects.get(pk=1)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        group.unique_name = request.data.get('unique_name', group.unique_name)
        group.display_name = request.data.get('display_name', group.display_name)
        group.save()
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        group.delete()
        res = {"code": 200, "message": "Delete Suessus!"}
        return Response(data=res, status=200)


@api_view(['GET'])
@csrf_exempt
def host_list(request):
    """
    List all hosts
    """
    if request.method == 'GET':
        tasks = Host.objects.all()
        serializer = HostSerializer(tasks, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def host_detail(request, pk):
    """
    Get,update or delete a specific host
    """
    try:
        host = Host.objects.get(pk=pk)
    except Host.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = HostSerializer(host)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        host.name = request.data.get('name',host.name)
        host.ip = request.data.get('ip',host.ip)
        host.save()
        serializer = HostSerializer(host)
        return JsonResponse(serializer.data)
    

@api_view(['GET'])
def count_groups(request):
    _groups = Group.objects.all()
    groups = []
    for group in _groups:
        if group is None:
            res = {"code": 400, "message": "Ops!, Don't find group by this id"}
            return Response(data=res,
                            status=400)
        group_apps = App.objects.filter(group_id=group.id).filter(enable=1).all()
        ok_num = 0
        warn_num = 0
        critical_num = 0
        for app in group_apps:
            if app.status == "OK":
                ok_num += 1
            elif app.status == "WARN":
                warn_num += 1
            elif app.status == "ERROR":
                critical_num += 1
        group_app = {"id": group.id,
                     "uniqueName": group.unique_name,
                     "displayName": group.display_name,
                     "statistics": {"total": len(group_apps),
                                    "OK".lower(): ok_num,
                                    "ERROR".lower(): critical_num,
                                    "WARN".lower(): warn_num,
                                    }
                     }
        groups.append(group_app)
        
    return Response(groups)
