from django import forms
from .models import Event, Attendance, Attendee, CheckIn

from django.forms import TextInput


class DateInput(forms.DateInput):
	input_type = 'date'

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['name','start_date', 'image', 'end_date', 'description', 'section', 'organization']
		widgets = {
		'start_date': DateInput(),
		'end_date': DateInput(),
	}


class AttendanceForm(forms.ModelForm):

	class Meta:
		model = Attendance
		fields = ['event', 'date', 'attendee']
		widgets = {
		'date': DateInput()
	}


class AttendeeForm(forms.ModelForm):

	class Meta:
		model = Attendee
		fields = ['name', 'email', 'date_registered', 'organization']
		widgets = {
		'date_registered': DateInput()
	}



class CheckInForm(forms.ModelForm):

	class Meta:
		model = CheckIn
		fields = ['name', 'access', 'event']
		









