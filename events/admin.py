from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from embed_video.admin import AdminVideoMixin
from .models import Event, Attendee, Attendance, CheckIn, Chat, EventContact, EventNotification, EventSubscriber, AppSubscriber

class EventAdmin(AdminVideoMixin, admin.ModelAdmin):
	list_display = ['name', 'start_date', 'end_date', 'organization','video']
	prepopulated_fields = {'slug':('name',)}

admin.site.register(Event, EventAdmin)



class AttendeeAdmin(admin.ModelAdmin):

	list_display = ['name', 'email', 'date_registered', 'organization']

admin.site.register(Attendee, AttendeeAdmin)




class CheckInAdmin(admin.ModelAdmin):

	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

	list_display = ['name', 'access', 'event', 'date']
	list_filter = ['name', 'access', 'event']

admin.site.register(CheckIn, CheckInAdmin)


class ChatRoomAdmin(admin.ModelAdmin):

	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

	list_display = ['event', 'author', 'date', 'upvote']
	list_filter = ['event']

admin.site.register(Chat, ChatRoomAdmin)




class AttendanceAdmin(admin.ModelAdmin):

	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

	list_display = ['event', 'attendee']
	list_filter = ['event']

admin.site.register(Attendance, AttendanceAdmin)


class EventContactAdmin(admin.ModelAdmin):

	list_display = ['name', 'email', 'date', 'subject', 'message',]

admin.site.register(EventContact, EventContactAdmin)


class EventNotificationAdmin(admin.ModelAdmin):

	list_display = ['event', 'info',]
	list_filter = ['event']

admin.site.register(EventNotification, EventNotificationAdmin)

class EventSubscriberAdmin(admin.ModelAdmin):

	list_display = ['event', 'email',]
	list_filter = ['event']

admin.site.register(EventSubscriber, EventSubscriberAdmin)

class AppSubscriberAdmin(admin.ModelAdmin):

	list_display = ['email',]

admin.site.register(AppSubscriber, AppSubscriberAdmin)


