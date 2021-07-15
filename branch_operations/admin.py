from django.contrib import admin
from django.db import models
from .models import FirstTimer, Convert, ServiceAttendance, ChurchBranch



class FirstTimerAdmin(admin.ModelAdmin):

	list_display = ['name', 'date', 'follow_up', 'occupation']
	list_filter = ['church_branch', 'follow_up', 'occupation']

admin.site.register(FirstTimer, FirstTimerAdmin)

class ConvertAdmin(admin.ModelAdmin):

	list_display = ['name', 'salvation_date', 'discipler', 'occupation']
	list_filter = ['church_branch', 'occupation']

admin.site.register(Convert, ConvertAdmin)

class ServiceAttendanceAdmin(admin.ModelAdmin):

	list_display = ['name', 'date', 'first_timers', 'total', 'date']
	list_filter = ['name', 'church_branch']

admin.site.register(ServiceAttendance, ServiceAttendanceAdmin)


class ChurchBranchAdmin(admin.ModelAdmin):

	list_display = ['name']
	list_filter = ['name']

admin.site.register(ChurchBranch, ChurchBranchAdmin)
