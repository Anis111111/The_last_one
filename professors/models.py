from django.db import models
from accounts.models import Profile

# Create your models here.


class Professor(models.Model):
    SPECIALIZATIONS = (
        ('networks', 'networks'),
        ('software', 'software'),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    phd_certificate = models.FileField(upload_to='certificates/')
    phd_date = models.DateField()
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS, default='software', verbose_name='specialization')

    def __str__(self):
        return self.profile.user.username