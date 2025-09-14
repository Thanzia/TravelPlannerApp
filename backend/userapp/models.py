from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

# Create your models here.

# CustomUserModel
class CustomUserModel(AbstractUser):

	email = models.EmailField(unique=True)

	phone_number = models.CharField(max_length=50)

	gender = models.CharField(max_length=50,choices=[('','select gender'),('male','male'),('female','female'),('others','others')])

	created_at = models.DateField(auto_now_add=True)

	def __str__(self):

		return self.username
	

# forgot password model
class ForgotPasswordModel(models.Model):

	email = models.EmailField()

	otp = models.CharField(max_length=10)

	created_at = models.DateTimeField(auto_now_add=True)

	def is_expired(self):
		
		return timezone.now() > self.created_at + timezone.timedelta(minutes=10)


