from django.shortcuts import render
import datetime
from django.utils import timezone
from events.models import Event, Attendee, CheckIn, Attendance, AppSubscriber
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


@permission_required('events.add_event')
def events_db(request):
	context = {
		'events': Event.objects.all(),
		'attendees': Attendee.objects.all(),
		'attendances': Attendance.objects.all()
	}
	return render(request, 'dashboard/events_db.html', context)


@permission_required('events.add_event')
def check_in_db(request, pk):
	check_ins = CheckIn.objects.filter(event=pk)
	event = Event.objects.get(pk=pk)
	attendances = Attendance.objects.filter(event=pk)

	if request.method == 'POST':
		name = request.POST.get('name')
		date = request.POST.get('date')
		time_limit = request.POST.get('mins')
		date = timezone.now().astimezone()
		date_format = '%a %b %d %Y %H:%M:%S'
		check_in = CheckIn.objects.get(name = name, event=pk)
		check_in.date = date
		check_in.time_limit = time_limit
		check_in.save()
		check_ins = CheckIn.objects.filter(event=pk)
		# event = Event.objects.get(pk=pk)
		context = {
		'check_ins': check_ins,
		'event':event,
		'attendances': attendances,
		}
		return render(request, 'dashboard/check_in_db.html', context)



	context = {
		'check_ins': check_ins,
		'event':event,
		'attendances': attendances,
	}
	return render(request, 'dashboard/check_in_db.html', context)


@permission_required('events.add_event')
def attendance_db(request):
	context = {
		# 'events': Event.objects.all(),
		# 'attends': Attend.objects.all(),
		# 'attendances': Attendance.objects.all()
	}
	return render(request, 'dashboard/attendance_db.html', context)


@permission_required('events.add_event')
def dashboard(request):

	context = {
		'events': Event.objects.all(),
		'attendees': Attendee.objects.all(),
		'check_ins': CheckIn.objects.all(),
		'subscribers': AppSubscriber.objects.all(),
	}
	return render(request, 'dashboard/dashboard.html', context)



@permission_required('events.add_event')
def registered_attendees(request, pk):
	check_ins = CheckIn.objects.filter(event=pk)
	event = Event.objects.get(pk=pk)
	attendances = Attendance.objects.filter(event=pk)


	context = {
		'check_ins': check_ins,
		'event':event,
		'attendances': attendances,
	}
	return render(request, 'dashboard/registered_attendees.html', context)


@permission_required('events.add_event')
def checkin_details(request, pk):
	check_ins = CheckIn.objects.get(pk=pk)
	# event = Event.objects.get(pk=pk)
	# attendances = Attendance.objects.filter(event=pk)


	context = {
		'check_ins': check_ins,
		# 'event':event,
		# 'attendances': attendances,
	}
	return render(request, 'dashboard/checkin_details.html', context)


def render_pdf_view(request, pk):
	# pk = kwargs.get('pk')
	# patient = get_object_or_404(Patient, pk=pk)

	check_ins = CheckIn.objects.get(pk=pk)

	template_path = 'dashboard/checkin_details_pdf.html'

	context = {
		'check_ins': check_ins,
	}
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="checkin_details.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)
	# create a pdf
	pisa_status = pisa.CreatePDF(html, dest=response)
	# if error then show some funy view
	if pisa_status.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
	return response