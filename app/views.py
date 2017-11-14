# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core import serializers
import os, datetime
from app.models import App, Update
from app.forms import UIForm
import sys, importlib

importlib.reload(sys)

# @login_required(login_url='/admin/login/?next=/admin/')

def index(request):
    return render(request, 'app/login.html')


def login(request):
    # if request.method == 'POST':
    #     form = UIForm.LoginForm(request.POST)
    #     if form.is_valid():
    #         username = request.POST['username']
    #         password = request.POST['password']
    #         user = auth.authenticate(username=username, password=password)
    #         if user is not None and user.is_active:
    #             auth.login(request, user)
    #             return render(request, 'app/index.html')
    #         else:
    #             return render_to_response('app/login.html')
    #     else:
    #         return render_to_response('app/login.html')
    # else:
    #     return render_to_response('app/login.html')
    apps = Update.objects.all()
    return render(request, 'app/index.html', {'apps': apps})


def app_add_page(request):
    return render(request, 'app/app_add.html')


def app_add(request):
    # getAppBaseInfo(os.getcwd() + "/appStorage/Smart360.apk")
    try:
        if request.method == 'POST':
            upload_file = request.FILES.get('file')
            appName = request.POST['appName']
            buildName = request.POST['buildName']
            version = request.POST['version']
            release_note = request.POST['releaseNote']
            if not upload_file:
                raise FileNotFoundError("please upload file")
            isExists = Update.objects.filter(app_name=appName, build_name=buildName)
            if isExists:
                return HttpResponse("添加失败，该应用以存在，请在更新列表中进行更新即可")

            name = upload_file.name[0:-4] + "_" + buildName + "_" + str(version) + ".apk"
            upload_file_path = os.getcwd() + "/appStorage/" + name
            with open(upload_file_path, 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            update = Update(app_name=appName, build_name=buildName, version=version, size=upload_file.size,
                            release_note=release_note, release_time=datetime.datetime, storage_name=name)
            update.save()
            app = App(app_name=appName, build_name=buildName, version=version, size=upload_file.size,
                      release_time=datetime.datetime, storage_name=name)
            app.save()
            return HttpResponse("Add application success")
        else:
            return HttpResponse("Must use the POST method")
    except Exception as e:
        return HttpResponse("Add application failed. >>> ")


# 获取同一 build_name 的 APP 信息
def app_list(request):
    if not request.method == 'GET':
        return HttpResponse("must use the GET method.")
    buildName = request.GET['buildName']
    apps = App.objects.filter(build_name__iexact=buildName).order_by('-version')
    return render(request, 'app/app_list.html', {'appList': apps, 'buildName': buildName})


def update_app_page(request):
    buildName = request.GET['buildName']
    update_app = Update.objects.get(build_name__exact=buildName)
    return render(request, 'app/update.html', {'app': update_app})


# 更新 APP
def upload_app(request):
    try:
        upload_file = request.FILES.get('file')
        version = request.POST['version']
        appName = request.POST['appName']
        buildName = request.POST['buildName']
        release_note = request.POST['releaseNote']
        if not upload_file:
            raise FileNotFoundError("please upload file.")
        updateApp = Update.objects.get(app_name=appName, build_name=buildName)
        if updateApp.version >= int(version):
            return HttpResponse("更新失败，新版本号小于当前版本")

        name = upload_file.name[:-4] + "_" + buildName + "_" + str(version) + ".apk"
        upload_file_path = os.getcwd() + "/appStorage/" + name
        with open(upload_file_path, 'wb+') as destination:
            for chunk in upload_file.chunks():
                destination.write(chunk)
        print(upload_file.size)
        updateApp.version = version
        updateApp.size = upload_file.size
        updateApp.release_note = release_note
        updateApp.release_time = datetime.datetime.now()
        updateApp.storage_name = name
        updateApp.save()

        app = App(app_name=appName, build_name=buildName, version=version, size=upload_file.size,
                  release_time=datetime.datetime, storage_name=name)
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
    # apps = App.objects.filter(app_name__exact=build_name).order_by('-version')[0:1]
    # for app in apps:
    #     print("app name: %s, version: %d" % (app.app_name, app.version))
    update = Update.objects.get(build_name__exact=build_name)
    if update:
        print(update.app_name)
    return HttpResponse(serializers.serialize('json', [update, ]))


# 下载 APP
def download_app(request):
    build_name = None
    if request.method == "POST":
        build_name = request.POST['buildName']
    elif request.method == "GET":
        build_name = request.GET["buildName"]
    if not build_name:
        raise RuntimeError("please add buildName and version parameter")
    print("%s" % build_name)
    apps = Update.objects.filter(build_name__exact=build_name)
    #apps = App.objects.get(build_name=build_name, version=version)
    storageName = None
    if apps:
        storageName = apps[0].storage_name
    if not storageName:
        raise RuntimeError("file not exist")

    # with open(os.getcwd() + "/appStorage/" + app_name, 'rb') as f:
    #     c = f.read()
    response = StreamingHttpResponse(read_file(os.getcwd() + "/appStorage/" + storageName))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(storageName)
    return response


def read_file(filename, buf_size=1024):
    with open(filename, "rb") as f:
        while True:
            content = f.read(buf_size)
            if content:
                yield content
            else:
                break


def getAppBaseInfo(apkPath):
    # 检查版本号等信息
    print(apkPath)
    output = os.popen(os.getcwd() + "/exters/aapt d badging %s" % apkPath)
    return output


# Create your views here.
