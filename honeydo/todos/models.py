from django.db import models
from django.conf import settings


class Access(models.Model):
    access_id = models.AutoField(primary_key=True)
    list = models.ForeignKey('Lists', models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    write = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Access'


class Lists(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=-1)
    list_description = models.CharField(max_length=-1, blank=True, null=True)
    list_owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Lists'


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    list = models.ForeignKey(Lists, models.DO_NOTHING)
    task_name = models.CharField(max_length=-1, blank=True, null=True)
    task_owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    due_date = models.DateField(blank=True, null=True)
    reset_time = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    repeat = models.IntegerField(blank=True, null=True)
    task_description = models.CharField(max_length=10485760, blank=True, null=True)
    task_completed_date = models.DateTimeField(blank=True, null=True)
    recur_ind = models.IntegerField(blank=True, null=True)
    recur_days = models.IntegerField(blank=True, null=True)
    parent_task_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tasks'
