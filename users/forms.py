from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class SignUpForm(UserCreationForm):
	email = forms.EmailField(
		max_length=100,
		required = True,
		help_text='Enter Email Address',
		widget=forms.TextInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'Email'}),
		)
	first_name = forms.CharField(
		max_length=100,
		required = True,
		help_text='Enter First Name',
		widget=forms.TextInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'First Name'}),
		)
	last_name = forms.CharField(
		max_length=100,
		required = True,
		help_text='Enter Last Name',
		widget=forms.TextInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'Last Name'}),
		)
	username = forms.CharField(
		max_length=200,
		required = True,
		help_text='Enter Username',
		widget=forms.TextInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'Username'}),
		)
	password1 = forms.CharField(
		help_text='Enter Password',
		required = True,
		widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'Password'}),
		)
	password2 = forms.CharField(
		required = True,
		help_text='Enter Password Again',
		widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill border-0 shadow-sm px-4', 'placeholder': 'Password Again'}),
		)

	class Meta:
		model = User
		fields = [
		'username', 'email', 'first_name', 'last_name', 'password1', 'password2',
		]




class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Creating a ProfileUpdateForm to update image
class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['image', 'address', 'position', 'church_branch']








