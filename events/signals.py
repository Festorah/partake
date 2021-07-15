from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Attendee, Attendance, CheckIn, Event, EventContact, EventNotification
import string
import random

#Generating random pins for the check_in
def pin_generator(size=5, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


#As the event is created, check_in is also been created with the number of sections filled in the form and each secion with its unique pin
@receiver(post_save, sender=Event)
def create_attendance(sender, instance, created, **kwargs):
	if created:
		event = Event.objects.get(pk=instance.pk)
		event.chat_pass = pin_generator()
		event.save()

		#Access pin is being generated
		for section in range(instance.section):
			access = pin_generator()
			new = CheckIn.objects.create(event=instance, name='Day '+ str(section+1), access=access, organization=instance.organization)
			new.save()

@receiver(post_save, sender=EventContact)
def event_notification(sender, instance, created, **kwargs):
	if created:
		event_contact = EventContact.objects.get(pk=instance.pk)
		event = event_contact.event
		event_name = event.name
		contact_name = event_contact.name
		
		new_notification = EventNotification.objects.create(event=event, info=f'{contact_name}, sent a message in the contact form.')
		new_notification.save()
