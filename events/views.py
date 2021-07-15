from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login


#For the forms
from users.models import Profile
from users.forms import SignUpForm
from django.contrib import messages
from .forms import EventForm, AttendanceForm, AttendeeForm, CheckInForm
from .models import Event, Attendance, Attendee, CheckIn, Chat, EventContact, AppSubscriber, EventSubscriber
import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

#These are needed for sending emails
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# The function for sending mail after every registration
def send_mail(reg, event):

	clients_name = reg.name
	clients_email = reg.email
	clients_event = event

	template = render_to_string('events/email_template.html', 
		{
		'name':clients_name,
		 'event':clients_event,
		 'email':clients_email,

		 })

	email = EmailMessage(
		f'Congratulations for Registering for our {clients_event}',
		template,
		settings.EMAIL_HOST_USER,
		[clients_email],
		)

	email.fail_silently=False 
	email.send()

	return True

def home(request):

	if request.method == 'POST':
		form  = SignUpForm(request.POST)

		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, f'Account was created for {user}')
			return redirect('profile_page')
		else:
			messages.error(request, 'Error Processing Your Request')
			context = {'form': form}
			return render(request, 'users/signup.html', context)

	events = Event.objects.all().order_by('start_date')
	attendees = Attendee.objects.all()
	registered_users = Profile.objects.all()
	sections = CheckIn.objects.all()
	context = {
		'events': events,
		'attendees': attendees,
		'registered_users': registered_users,
		'sections': sections,
	}

	return render(request, 'events/index.html', context)


def services(request):
	return render(request, 'events/services.html')


def about(request):

	if request.method == 'POST':

		#Do something for the about page...to be added later

		return render(request, 'events/about.html')
	return render(request, 'events/about.html')


def contact(request):
	return render(request, 'events/contact.html')


def register(request):
	return render(request, 'events/event_reg.html')

def events(request):
	return render(request, 'events/events.html')


def add_events(request):

	if request.method == 'POST':

		#Instantiating the form
		e_form  = EventForm(request.POST, request.FILES)

		if e_form.is_valid():
			e_form.save()
			messages.success(request, 'Event was created')
			return redirect('profile_page')

		else:
			messages.error(request, 'Error Processing Your Request')
			context = {'e_form': e_form}
			return render(request, 'events/add_events.html', context)

	e_form = EventForm()
	context = {'e_form': e_form}
	return render(request, 'events/add_events.html', context)



def events_list(request):

	events = Event.objects.all().order_by('-start_date')#Ordering according to date
	context = {
		'events': events
	}
	return render(request, 'events/events_list.html', context)

def search(request):
	events = Event.objects.all().order_by('-start_date')

	if 'name' in request.GET:
		name = request.GET['name']
		if name:
			events = events.filter(name__icontains=name)

	context = {
		'events': events,
	}
	for event in events:
		print(event.name)
	return render(request, 'events/search.html', context)



def event_reg(request, pk):

	# This is for User registration
	if request.user.is_authenticated:  
		event = Event.objects.get(pk=pk)

		#This is to be sure that no account has been created with this name and email
		if not event.attendee.filter(email=request.user.email, name = request.user.username).exists(): 
			reg = event.attendee.create(user=request.user, name= request.user.username, email = request.user.email)

			# Sending congratulatory mail for event registration
			send_mail(reg, event)

			messages.success(request, f'You have successfully registered for {event}')
			return redirect('profile_page')
		else:
			messages.error(request, f'You cannot register for {event} more than once')
			return redirect('profile_page')

	#This is for non-user registration
	else:
		atd_form = AttendeeForm()
		event = Event.objects.get(pk=pk)
		context = {
					'atd_form': atd_form,
					'event': event,
				}

		if request.method == 'POST':
			atd_form  = AttendeeForm(request.POST)

			if atd_form.is_valid():
				name = atd_form.cleaned_data.get('name')
				email = atd_form.cleaned_data.get('email')
				date_registered = atd_form.cleaned_data.get('date_registered')
				organization = atd_form.cleaned_data.get('organization')
				event = Event.objects.get(pk=pk)

				#This is to be sure that no account has been created with this name and email
				if not event.attendee.filter(email=email).exists():
					reg = event.attendee.create(name=name, email=email, organization=organization, through_defaults={'date':date_registered})
					reg.save()

					# Sending congratulatory mail for event registration 
					send_mail(reg, event)

					messages.success(request, f'You have successfully registered for {event}')
					return render(request, 'events/event_reg.html', context)
				else:
					messages.error(request, f'You already have successfully registered for {event}')
					return render(request, 'events/event_reg.html', context)
			else:
				messages.error(request, f'Please check the form and makesure all the fields are filled appropriately')
				return render(request, 'events/event_reg.html', context)

		return render(request, 'events/event_reg.html', context)


def check_in(request):

	if request.method == 'POST':
		name = request.POST.get('name')
		date = request.POST.get('start_date')
		email = request.POST.get('email')
		pin = request.POST.get('pin')
		organization = request.POST.get('organization')
		date_string = date.split(' G')[0]
		date_format = '%a %b %d %Y %H:%M:%S'
		date_obj = datetime.datetime.strptime(date_string, date_format).astimezone()
		try:
			check_in = CheckIn.objects.get(access = pin, organization=organization)
			check_in_time_limit = check_in.time_limit #This is to get the time_limit for the check_in day
			check_in_event = check_in.event
			date_check_in = check_in.date


			check_in_access = date_obj - date_check_in #This is the time difference between the check_in time and the time set by the admin
			allow_check_in_access = check_in_access.total_seconds() / 60 #This converts the time difference to minutes

			#Conditional statement to check if the time difference is not more than the time_limit set by the admin
			if allow_check_in_access < check_in_time_limit:
				event = Event.objects.get(name=check_in_event)
				attendee = event.attendee.get(email=email)

				# attendee = Attendee.objects.get(email=email, organization=organization) #Email addresses are unique 
				attendance = Attendance.objects.get(attendee = attendee.pk)
				event = attendance.event
				attendance.check_in.add(check_in)
				check_in.reg_attendee.add(attendee)
				messages.success(request, f'You have successfully checked_in for {check_in} {event}')
				return render(request, 'events/check_in.html')
			else:
				messages.error(request, 'There is no ongoing event')
				return render(request, 'events/check_in.html')

		except ObjectDoesNotExist as DoesNotExist:
			messages.error(request, f'You are not yet registered. Please contact admin. Thank you')
			return render(request, 'events/check_in.html')

	return render(request, 'events/check_in.html')

def event_sub(request, slug):

	event = Event.objects.get(slug=slug)
	name = event.name
	context = {'event': event}

	if request.method == 'POST':
		
		#Getting all the needed parameters from the user
		email = request.POST.get('email_sub')
		subscriber = EventSubscriber.objects.create(event=event, email=email)
		subscriber.save()
		return render(request, 'events/event_detail_2.html', context)
	return render(request, 'events/event_detail_2.html', context)


def app_sub(request):
	if request.method == 'POST':
		
		#Getting all the needed parameters from the user
		email = request.POST.get('email')
		subscriber = AppSubscriber.objects.create(email=email)
		subscriber.save()
		redirect ('home')
	return render(request, 'events/index.html')



def event_detail(request, slug):

	event = Event.objects.get(slug=slug)
	context = {'event': event}

	if request.method == 'POST':
		
		#Getting all the needed parameters from the user
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		contact = EventContact.objects.create(event=event, name=name, email=email, subject=subject, message=message)
		contact.save()
		return render(request, 'events/event_detail_2.html', context)
			
	return render(request, 'events/event_detail_2.html', context)





def chat_room(request, pk):
	event = Event.objects.get(pk=pk)

	if request.method == 'POST':

		email = request.POST.get('email')
		chat_pass = request.POST.get('chat_pass')
		event = Event.objects.get(pk=pk)
		event_pass = event.chat_pass

		if chat_pass == event_pass:
			chat_room = Chat.objects.filter(event=event).order_by('date')
			attendees = Attendee.objects.filter(event=event)
			user = Attendee.objects.get(event=event, email=email)#This is to get the attendee's details for chat messaging and for the upvotes
			context = {
				'chat_room': chat_room,
				'attendees': attendees,
				'event': event,
				'user': user
			}
			return render(request, 'events/chatroom.html', context)

	context = {'event': event}
	return render(request, 'events/event_detail.html', context)


#This is for the instant messaging in the chat room...works together with the ajax form in the template
def chat_room_message(request):

	if request.method == 'POST':


		#Getting the necessary details from the user
		message = request.POST.get('message')
		event = request.POST.get('event')
		user = request.POST.get('userch')
		event = Event.objects.get(name=event)
		attendee = Attendee.objects.get(event = event, name = user)
		author = attendee.name

		chat_room_message = Chat.objects.create(event=event, author=attendee, message=message)

		if message!='': #Just to be sure that the message about to be sent is not an empty string
			chat_room_message.save()
		return JsonResponse({ 'message': message, 'author': author}) #This returns a Json which is to feed the ajax function in the templates

def upvote(request, slug):
	event = Event.objects.get(slug=slug)

	if request.method == 'POST':
		
		#Getting all the needed parameters from the user
		upvote_count = request.POST.get('upvote_count')
		event = request.POST.get('event')
		chati_message = request.POST.get('chati_message')
		pk = request.POST.get('chati_pk')
		user = request.POST.get('user')
		event = Event.objects.get(name=event)
		attendee = Attendee.objects.get(event =event, name = user)
		author = attendee
		chat_room_message = Chat.objects.get(event=event.pk, message=chati_message, pk=pk)

		#For user not to upvote a message more than once
		if attendee not in chat_room_message.voters.all():
			updated_upvote =int(upvote_count) + 1
			chat_room_message.upvote = updated_upvote
			chat_room_message.voters.add(attendee)
			chat_room_message.save()
		else:
			messages.error(request, 'You cannot upvote a message twice')



		#This can be changed later if the ajax can be modified to accomodate when the user wants to upvote more than once


		chat_room = Chat.objects.filter(event=event).order_by('date')
		attendees = Attendee.objects.filter(event=event)
		user = Attendee.objects.get(event=event, email=attendee.email)

		context = {
			'chat_room': chat_room,
			'attendees': attendees,
			'event': event,
			'user': user
		}
		return render(request, 'events/chatroom.html', context)
	context = {'event': event}
	return render(request, 'events/chatroom.html', context)


def event_contact(request):

	if request.method == 'POST':
		
		#Getting all the needed parameters from the user
		upvote_count = request.POST.get('upvote_count')
		event = request.POST.get('event')
		chati_message = request.POST.get('chati_message')
		user = request.POST.get('user')
		event = Event.objects.get(name=event)
		attendee = Attendee.objects.get(event =event, name = user)
		author = attendee
		chat_room_message = Chat.objects.get(event=event.pk, message=chati_message)

	event = Event.objects.get()
	context = {'event': event}
	return render(request, 'events/event_detail_2.html', context)



def blog_detail(request):
	return render(request, 'events/blog_detail.html')
