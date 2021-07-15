from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .choices import POSITION
from branch_operations.models import ChurchBranch


# class User(AbstractUser):
#     pass

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	address = models.TextField(default='You should update your address here...could be anywhere in the world')
	position = models.CharField(max_length=250, choices=POSITION, blank=True)
	church_branch = models.ForeignKey(ChurchBranch, on_delete=models.CASCADE, blank=True, null=True)
	dashboard_pass_1 = models.CharField(max_length=10, blank=True, default='glory')
	dashboard_pass_2 = models.CharField(max_length=10, blank=True, default='peace')

	def __str__(self):
		return f"{self.user.username} Profile"

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.image.path)


		if img.height> 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

