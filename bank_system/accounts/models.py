from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
	telegram_id = models.BigIntegerField()

	REQUIRED_FIELDS = ["telegram_id"]
