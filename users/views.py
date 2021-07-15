from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, authenticate, logout
from django.contrib import messages 
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from events.models import Event, Attendee, Attendance


def signup(request):

	form = SignUpForm()
	context = {'form': form}
	return render(request, 'users/signup.html', context)



def LoginPage(request):

	if request.method == 'POST':

		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			django_login(request, user)
			return redirect('profile_page')
	context = {}
	return render(request, 'users/login.html', context)



def services(request):
	return render(request, 'events/services.html')


def LogoutPage(request):

	logout(request)
	return redirect('LoginPage')

@login_required(login_url='LoginPage')
def profile_page(request):

	if request.method == 'POST':
		# Instatiating both the user form and the profile form
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,
									request.FILES,
									instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile_page')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		
	user_attendee = Attendee.objects.filter(name=request.user.username)
	reg_event_number = user_attendee.all().count()
	reg_event_names = list()
	for me in user_attendee:
		reg_event_names.append(me.event_set.all().first())

	context = {
		'u_form': u_form,
		'p_form': p_form,
		'user_attendee': user_attendee,
		'reg_event_names':reg_event_names,
	}

	return render(request, 'users/profile_page2.html', context)


