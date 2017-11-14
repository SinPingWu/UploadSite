from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    nick_name = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nick_name


class App(models.Model):
    app_name = models.CharField(max_length=20)
    build_name = models.CharField(max_length=20, default="")
    version = models.IntegerField()
    size = models.BigIntegerField()
    release_time = models.DateTimeField(auto_now_add=True)
    storage_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.app_name


class Update(models.Model):
    app_name = models.CharField(max_length=20)
    build_name = models.CharField(max_length=20, unique=True)
    version = models.IntegerField()
    size = models.BigIntegerField()
    release_note = models.TextField(max_length=200)
    release_time = models.DateTimeField(auto_now_add=True)
    storage_name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.app_name

    def toJson(self):
        import json
        return json.dump(dict([(attr, getattr(self, attr)) for attr
                               in [f.name for f in self._meta.fields]]))

# Create your models here.
