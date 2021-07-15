from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from .models import Profile

admin.site.site_header = "THE DREAM CENTRE OF THE LIFEOASIS INT'L CHURCH"


class ProfileAdmin(admin.ModelAdmin):

	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

	list_display = ['user','position', 'church_branch']
	list_filter = ['position']

admin.site.register(Profile, ProfileAdmin)

