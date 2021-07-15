from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ServiceAttendanceForm, ConvertForm, FirstTimerForm
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import permission_required
from .models import FirstTimer, Convert, ServiceAttendance, ChurchBranch


# Create your views here.
def first_timers(request):

	if request.method == 'POST':

		f_form  = FirstTimerForm(request.POST)

		if f_form.is_valid():
			f_form.save()
			messages.success(request, f'You have successfully registered the first timer')
			return render(request, 'branch_operations/first_timers.html', context)
		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/first_timers_form.html', context)


	f_form = FirstTimerForm()
	context = {
				'f_form': f_form,
			}
	return render(request, 'branch_operations/first_timers_form.html', context)

def converts(request):
	c_form = ConvertForm()
	context = {
				'c_form': c_form,
			}
	if request.method == 'POST':
		c_form = ConvertForm(request.POST)
		if c_form.is_valid():
			c_form.save()
			messages.success(request, f'Report sent!')
			return render(request, 'branch_operations/converts.html', context)
		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/converts.html', context)
	return render(request, 'branch_operations/converts_form.html', context)



def service_attendance(request):
	s_form = ServiceAttendanceForm()
	context = {
				's_form': s_form,
			}
	if request.method == 'POST':
		s_form  = ServiceAttendanceForm(request.POST)
		if s_form.is_valid():
			s_form.save()
			messages.success(request, f'Report sent!')
			return render(request, 'branch_operations/service_attendance.html', context)
		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/service_attendance.html', context)
	# atd_form = AttendeeForm()
	# context = {'atd_form': atd_form}
	return render(request, 'branch_operations/service_attendance_form.html', context)

@permission_required('branch_operations.add_convert')
def branch_dashboard(request):


	church_branch = ChurchBranch.objects.get(name = request.user.profile.church_branch)
	
	if request.method == 'POST':
		s_form  = ServiceAttendanceForm(request.POST)
		if s_form.is_valid():
			s_form.save()
			messages.success(request, f'Report sent!')
			return render(request, 'branch_operations/service_detail_db.html', context)

		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/service_detail_db.html', context)

	#It's only pastor of the branch that can view the branch's Dashboard

	elif church_branch.pastor.username == request.user.username:

		first_timers = FirstTimer.objects.filter(church_branch=request.user.profile.church_branch).order_by('-date')
		converts = Convert.objects.filter(church_branch=request.user.profile.church_branch).order_by('-salvation_date')
		service_attendance = ServiceAttendance.objects.filter(church_branch=request.user.profile.church_branch).order_by('-date')
		# service_name = service_attendance[0].name
		s_form  = ServiceAttendanceForm()

		context = {
			'first_timers': first_timers,
			'converts': converts,
			'service_attendance':service_attendance,
			# 'service_name':service_name,
			's_form':s_form
		}
		return render(request, 'branch_operations/branch_operations_dashboard.html', context)

	else:
		messages.error(request, 'You do not have the permission to view this page please contact the admin')
		return redirect('profile_page')





	# return render(request, 'branch_operations/branch_operations_dashboard.html', context)


def new_converts_db(request):

	c_form = ConvertForm()
	new_converts = Convert.objects.filter(church_branch=request.user.profile.church_branch).order_by('-salvation_date')
	context = {
		'new_converts': new_converts,
		'c_form':c_form,
	}
	if request.method == 'POST':

		c_form  = ConvertForm(request.POST)

		if c_form.is_valid():
			c_form.save()
			messages.success(request, f'You have successfully registered the new convert')
			return render(request, 'branch_operations/new_converts_db.html', context)
		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/new_converts_db.html', context)


	return render(request, 'branch_operations/new_converts_db.html', context)


def first_timers_db(request):

	f_form = FirstTimerForm()
	first_timers = FirstTimer.objects.filter(church_branch=request.user.profile.church_branch).order_by('-date')
	context = {
				'f_form': f_form,
				'first_timers': first_timers,
			}

	if request.method == 'POST':

		f_form  = FirstTimerForm(request.POST)

		if f_form.is_valid():
			f_form.save()
			messages.success(request, f'You have successfully registered the first timer')
			return render(request, 'branch_operations/first_timers_db.html', context)
		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/first_timers_db.html', context)

	return render(request, 'branch_operations/first_timers_db.html', context)

def service_detail(request, pk):

	service_attendance = ServiceAttendance.objects.filter(pk=pk).order_by('-date')
	service_name = service_attendance[0].name
	s_form  = ServiceAttendanceForm()
	context = {
		'service_attendance':service_attendance,
		'service_name':service_name,
		's_form':s_form
	}

	if request.method == 'POST':
		s_form  = ServiceAttendanceForm(request.POST)
		if s_form.is_valid():
			s_form.save()
			messages.success(request, f'Report sent!')
			return render(request, 'branch_operations/service_detail_db.html', context)

		else:
			messages.error(request, 'Error Processing Your Request')
			return render(request, 'branch_operations/service_detail_db.html', context)

	return render(request, 'branch_operations/service_detail_db.html', context)