from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, null=False, blank=False)

    def __str__(self):
        return self.username

class VerificationCodes(models.Model):
    email=models.EmailField()
    code = models.IntegerField()
    is_recovery = models.BooleanField(null=True)

    time_create=models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    EXPIRY_MINUTES = 5

    def save(self,*args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=self.EXPIRY_MINUTES)
        super().save(*args, **kwargs)



    class Meta:
        ordering = ['time_create']



