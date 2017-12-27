# coding=utf-8

from django.db import models
# from datetime import datetime
from django.utils import timezone as datetime


# Create your models here.
class App(models.Model):
    class Meta:
        db_table = 'app'

    name = models.CharField(max_length=128)
    host_id = models.IntegerField()
    group_id = models.IntegerField()
    configuration = models.TextField()
    status = models.CharField(max_length=12)
    message = models.TextField()
    enable = models.IntegerField()
    last_update = models.DateTimeField()
    
    @classmethod
    def create(cls, name, host_id, status, message, enable, group_id):
        app = cls(name=name, host_id=host_id, status=status, message=message, enable=enable, group_id=group_id,
                  last_update=datetime.now())
        return app


class AppStatistics(models.Model):
    class Meta:
        db_table = 'app_statistics'

    app_id = models.IntegerField()
    statistics = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, app_id, statistics):
        app_statistics = cls(app_id=app_id, statistics=statistics)
        return app_statistics


class AppHistory(models.Model):
    class Meta:
        db_table = 'app_history'

    app_id = models.IntegerField()
    status = models.CharField(max_length=32)
    message = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)

    def convert_to_epoc(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, app_id, status, message):
        group = cls(app_id=app_id, status=status,message=message)
        return group


class Group(models.Model):
    class Meta:
        db_table = 'app_group'

    unique_name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32)

    @classmethod
    def create(cls, unique_name, display_name):
        group = cls(unique_name=unique_name, display_name=display_name)
        return group


class Host(models.Model):
    class Meta:
        db_table = 'app_host'

    name = models.CharField(max_length=32)
    ip = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True)

    @classmethod
    def create(cls, ip, name=''):
        group = cls(ip=ip, name=name)
        return group
