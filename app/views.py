from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
import os, datetime
from app.models import User, App


@login_required(login_url='/admin/login/?next=/admin/')
def upload_app_page(request):
    return render(request, 'app/upload.html')


# 更新 APP
def upload_app(request):
    try:
        upload_file = request.FILES.get('file')
        version = request.POST['version']
        build_name = request.POST['buildName']
        if not upload_file:
            raise FileNotFoundError("please upload file.")
        name = upload_file.name
        upload_file_path = os.getcwd() + "/appStorage/" + name
        with open(upload_file_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        print(upload_file.size)
        app = App(app_name=name, version=version, size=upload_file.size, release_time=datetime.datetime, build_name=build_name)
        app.save()
    except BaseException as e:
        return HttpResponse(e)

    return HttpResponse("upload success")


# 获取升级信息
def get_update_info(request):
    build_name = None
    if request.method == "POST":
        build_name = request.POST['buildName']
    elif request.method == "GET":
        build_name = request.GET["buildName"]
    if not build_name:
        raise RuntimeError("please add buildName parameter")
    apps = App.objects.filter(app_name__exact=build_name).order_by('-version')[0:1]
    # for app in apps:
    #     print("app name: %s, version: %d" % (app.app_name, app.version))
    if apps:
        app = apps[0]
        print(app.app_name)
    return HttpResponse("get update info success")


# 下载 APP
def download_app(request):
    build_name = None
    version = 0
    if request.method == "POST":
        build_name = request.POST['buildName']
        version = request.POST['version']
    elif request.method == "GET":
        build_name = request.GET["buildName"]
        version = request.GET['version']
    if not build_name or not version:
        raise RuntimeError("please add buildName and version parameter")
    print("%s, %s" % (build_name, version))
    apps = App.objects.filter(build_name__exact=build_name, version=version)
    #apps = App.objects.get(build_name=build_name, version=version)
    app_name = None
    if apps:
        app_name = apps[0].app_name
    if not app_name:
        raise RuntimeError("file not exist")

    # with open(os.getcwd() + "/appStorage/" + app_name, 'rb') as f:
    #     c = f.read()
    response = StreamingHttpResponse(read_file(os.getcwd() + "/appStorage/" + app_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(app_name)
    return response
    return HttpResponse(c)


def read_file(filename, buf_size=1024):
    with open(filename, "rb") as f:
        while True:
            content = f.read(buf_size)
            if content:
                yield content
            else:
                break


def app_list(request):
    return HttpResponse("search list success")
# Create your views here.
