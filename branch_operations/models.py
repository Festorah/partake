from django.db import models
from users.choices import POSITION
from django.contrib.auth.models import User


class ChurchBranch(models.Model):
	name = models.CharField(max_length=250, blank=True)
	pastor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return str(self.name)




class FirstTimer(models.Model):
	name = models.CharField(max_length=100)
	date = models.DateTimeField()
	address = models.TextField(default='address!')
	church_branch = models.ForeignKey(ChurchBranch, on_delete=models.CASCADE, blank=True)
	follow_up = models.CharField(max_length=50)
	report = models.TextField(blank = True, default='')
	phone_number = models.CharField(max_length=15, blank=True)
	occupation = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return str(self.name)


class Convert(models.Model):
	name = models.CharField(max_length=100)
	salvation_date = models.DateTimeField()
	address = models.TextField(default='Come all things are Ready. Jesus is Lord!')
	church_branch = models.ForeignKey(ChurchBranch, on_delete=models.CASCADE, blank=True)
	discipler = models.CharField(max_length=50)
	report = models.TextField(blank = True, default='')
	phone_number = models.CharField(max_length=15, blank=True)
	occupation = models.CharField(max_length=50, blank=True)

	def __str__(self):
		return str(self.name)


class ServiceAttendance(models.Model):
	name = models.CharField(max_length=100)
	date = models.DateTimeField()
	church_branch = models.ForeignKey(ChurchBranch, on_delete=models.CASCADE, blank=True)
	pastor = models.IntegerField()
	men = models.IntegerField()
	women = models.IntegerField()
	brothers = models.IntegerField()
	sisters = models.IntegerField()
	teenagers = models.IntegerField()
	children = models.IntegerField()
	first_timers = models.IntegerField()
	total = models.IntegerField()
	pastors_comments = models.TextField(blank = True, default='')
	dashboard_pass_1 = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return str(self.name)