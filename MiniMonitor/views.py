from django.http import HttpResponse
import sys


def homepage(request):
    response = HttpResponse(open(sys.path[0] + "/monitor/templates/index.html"))
    return response


def manager(request, appid):
    return HttpResponse(open(sys.path[0] + "/monitor/templates/manager.html"))
