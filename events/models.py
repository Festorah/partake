from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify




class Attendee(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField( blank=True)
	date_registered = models.DateTimeField(default=timezone.now)
	organization = models.CharField(max_length=200, default='THE DREAM CENTRE CHURCH', blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


	class Meta:
		ordering = ['name']
	

	def __str__(self):
		return str(self.name)



class Event(models.Model):
	name = models.CharField(max_length=100)
	organization = models.CharField(max_length=200, default='THE DREAM CENTRE CHURCH') 
	start_date = models.DateTimeField(blank=True, null=True)
	end_date = models.DateTimeField(blank=True, null=True)
	image = models.ImageField(default='event_default.jpg', upload_to='event_pics', blank=True)
	description = models.TextField(default='Come all things are Ready. Jesus is Lord!')
	attendee = models.ManyToManyField(Attendee, through='Attendance')
	section = models.IntegerField(default=5, blank=True, null=True)
	chat_intro = models.TextField(default='Come all things are Ready. Jesus is Lord!')
	video = EmbedVideoField(blank=True)
	chat_pass = models.CharField(max_length=50, blank=True)
	slug = models.SlugField(null=False, unique=True)
	
	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('event_detail', kwargs={'slug':self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)

class CheckIn(models.Model):
	name = models.CharField(max_length=50)
	access = models.CharField(max_length=20, blank=True, null=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	organization = models.CharField(max_length=200, default='THE DREAM CENTRE CHURCH')
	reg_attendee = models.ManyToManyField(Attendee, blank=True)
	date = models.DateTimeField(default=timezone.now)
	time_limit = models.IntegerField(blank=True, default=15, null=True)

	def __str__(self):
		return str(self.name)

		

class Attendance(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
	attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name='attendee_main', blank=True, null=True)
	date = models.DateTimeField(blank=True, null=True)
	check_in = models.ManyToManyField(CheckIn, blank=True)
	# reg_event = models.ManyToManyField(Event, blank=True, related_name='reg_event')




	class Meta:
		ordering = ['attendee']
		unique_together = [['attendee', 'event']]

	def __str__(self):
		return str(self.attendee)




class Chat(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(Attendee, on_delete=models.CASCADE, blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	message = models.TextField(default='Come all things are Ready. Jesus is Lord!', null=True)
	upvote = models.CharField(max_length=10, default='5a', blank=True, null=True)
	voters = models.ManyToManyField(Attendee, related_name='voters', blank=True)

	def __str__(self):
		return str(self.event.name)


class EventContact(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	date = models.DateTimeField(default=timezone.now)
	subject = models.CharField(max_length=250, default='subject', blank=True, null=True)
	message = models.TextField()

	def __str__(self):
		return str(self.name)


class EventNotification(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)
	info = models.CharField(max_length=250, blank=True, null=True)

	def __str__(self):
		return str(self.event.name)

class EventSubscriber(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	email = models.EmailField()

	def __str__(self):
		return str(self.event.name)

class AppSubscriber(models.Model):
	email = models.EmailField()

	def __str__(self):
		return str(self.name)