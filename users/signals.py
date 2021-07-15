from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from branch_operations.models import ChurchBranch
import string
import random

#Generating random unique pins for the each profile
def pin_generator(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		print('coming')
		for x in range(2):
			if x == 0:
				dashboard_pass_1 = pin_generator()
			else:
				dashboard_pass_2 = pin_generator()
		Profile.objects.create(user=instance, dashboard_pass_1=dashboard_pass_1, dashboard_pass_2=dashboard_pass_2)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()
