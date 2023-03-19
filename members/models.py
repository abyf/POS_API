from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timezone

class User(AbstractUser):
	name = models.CharField(max_length=120)
	phone = models.CharField(max_length=20, unique=True)
	
	def __str__(self):
		return "{name}:{phone}".format(name=self.name,phone=self.phone)


