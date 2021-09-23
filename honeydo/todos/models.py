from django.db import models
from django.conf import settings


class Access(models.Model):
    access_id = models.AutoField(primary_key=True)
    list = models.ForeignKey('Lists', models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    write = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Access'
        verbose_name_plural = "Access"

    def __str__(self):
        txt = self.list.list_name + "->" + self.user.username 
        return txt


class Lists(models.Model):
    list_id = models.AutoField(primary_key=True)
    list_name = models.CharField(max_length=200)
    list_description = models.CharField(max_length=1000, blank=True, null=True)
    list_owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)

    def __str__(self):
        return self.list_name

    class Meta:
        managed = False
        db_table = 'Lists'
        verbose_name_plural = "Lists"


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    list = models.ForeignKey(Lists, models.DO_NOTHING)
    task_name = models.CharField(max_length=200, blank=True, null=True)
    task_owner = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
    due_date = models.DateField(blank=True, null=True)
    reset_time = models.DateTimeField(blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True, related_name="assigned_user")
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, blank=True, null=True, related_name="completed_by")
    points = models.IntegerField(blank=True, null=True)
    repeat = models.IntegerField(blank=True, null=True)
    task_description = models.CharField(max_length=10485760, blank=True, null=True)
    task_completed_date = models.DateTimeField(blank=True, null=True)
    recur_ind = models.IntegerField(blank=True, null=True)
    recur_days = models.IntegerField(blank=True, null=True)
    parent_task_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.task_name

    class Meta:
        managed = False
        db_table = 'Tasks'
        verbose_name_plural = "Tasks"
