from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User

from .models import Tasks
from .models import Lists
from .models import Access

# class customListAddForm(forms.ModelForm):
#     new_task = forms.CharField()

#     def save(self, commit=True):
#         new_task =  self.cleaned_data.get("new_task", None)
#         list = self.cleaned_data.get("list_name", None)
#         task_owner = self.cleaned_data.get("list_owner", None)
#         newTask = Tasks(list = list, task_name = new_task, task_owner = task_owner) 
#         newTask.save() 
#         return super(customListAddForm, self).save(commit=commit)
    
#     class Meta:
#         model = Lists
#         fields = "__all__"


class customTaskAddForm (forms.ModelForm):
    user_access = forms.ModelChoiceField(queryset=User.objects.all())

    def save(self, commit=True):
        user_access = self.cleaned_data.get("user_access", None)
        list_name = self.cleaned_data.get("list", None)
        new_access = Access(list = list_name, user = user_access)
        new_access.save()
        return super(customTaskAddForm, self).save(commit=commit)

    class Meta:
        model = Tasks
        fields = "__all__"

class ListAdmin(admin.ModelAdmin):

    # form = customListAddForm

    actions = None
    
    list_display = ("list_name", "get_task_count", "list_description", "list_owner")
    list_editable = ("list_owner",)
    list_filter = ("list_owner",)
  
    fields = ("list_name", "list_description", "list_owner")


    def get_task_count(self, obj):
        return obj.tasks_set.count()
    get_task_count.short_description = "Count of Tasks"

    search_fields = ["list_name"]

class TaskAdmin(admin.ModelAdmin):

    form = customTaskAddForm
    
    list_display = ("task_name", "get_state", "get_list_link", "due_date", "assigned_user")
    list_editable = ("assigned_user", "due_date")
    list_filter=("assigned_user", "list__list_name")

    list_display_links = ("task_name", "get_list_link")

    fieldsets = (
        (None, {
            "fields": ("list", "task_name", "task_owner", "task_description", "user_access")
        }),
        ("Advanced options", {
            "classes": ("collapse",),
            "fields": ("due_date", "assigned_user", "points", "repeat")
        })
    )
    
    ordering = ["due_date"]
    search_fields = ["task_name"]

    actions = ["claim_task", "make_active", "make_inactive"]

    def get_list_link(self, obj):
        return format_html("<a href='%s'>%s</a>" % (reverse("admin:todos_lists_change", args=[obj.list_id]), obj.list))

    get_list_link.short_description = "Lists"
    get_list_link.allow_tags = True


    def get_state(self, obj):
        return obj.state == 0
    get_state.boolean = True
    get_state.short_description = "Status"

    @admin.action(description="Make Active")
    def make_active(modeladmin, request, queryset):
        queryset = queryset.exclude(state = 0)
        queryset.update(state = 0)
        messages.success(request, "Selected Task(s) Marked as Active")
    
    @admin.action(description="Make In-active")
    def make_inactive(modeladmin, request, queryset):
        queryset = queryset.exclude(state = 1)
        queryset.update(state = 1)
        queryset.update(completed_by = request.user.id)
        messages.success(request, "Selected Task(s) Marked as In Active")
    
    @admin.action(description="Claim Task")
    def claim_task(modeladmin, request, queryset):
        queryset.update(assigned_user = request.user.id)
        messages.success(request, "Selected Task(s) have been assigned to you")

    date_hierarchy = "due_date"

admin.site.register(Tasks, TaskAdmin)
admin.site.register(Lists, ListAdmin)
admin.site.register(Access)

