from django import forms
from django.forms import TextInput, Select, Textarea, DateInput
from .models import FirstTimer, Convert, ServiceAttendance

class DateInput(forms.DateInput):
	input_type = 'date'

class FirstTimerForm(forms.ModelForm):

	class Meta:
		model = FirstTimer
		fields = ['name','date', 'follow_up', 'address', 'church_branch', 'report', 'occupation','phone_number']
		widgets = {
		'date': DateInput(),
	}


class ConvertForm(forms.ModelForm):

	class Meta:
		model = Convert
		fields = '__all__'
		widgets = {
		'salvation_date': DateInput()
	}


class ServiceAttendanceForm(forms.ModelForm):

	class Meta:
		model = ServiceAttendance
		fields = ['name','date', 'church_branch','pastor', 'men',  'women', 'brothers','sisters','teenagers', 'children', 'first_timers', 'total', 'pastors_comments']
		widgets = {
		'date': DateInput()
	}



