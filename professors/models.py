from django.dispatch import receiver
from django.db.models.signals import post_save ,pre_save
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

@receiver(post_save, sender=Professor)
def save_profile(sender, instance, created, **kwargs):
    try:
        profile = instance.profile
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
