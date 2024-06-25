from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save ,pre_save
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    id = models.AutoField(primary_key=True)
    reset_password_token = models.CharField(max_length=50, default="", null=True, blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)
    
    img = models.ImageField(upload_to='photos/', height_field='height', width_field='width', null=True, blank=True)  # user_upload_to
    height = 5 # models.PositiveIntegerField(default=5)
    width = 5 # models.PositiveIntegerField(default=5)

    phone = models.CharField(max_length=10, null=True, unique=True,
                            validators=[
                                RegexValidator(
                                                regex=r'^\d{10}$',
                                                message='The phone must be 10 numbers long.',
                                                code='invalid_phone'
                                ),
                            ])
    address = models.CharField(max_length=50 , blank=True,null=True)
    age = models.PositiveIntegerField(default=19,
        validators=[
                    MinValueValidator(19),
                    MaxValueValidator(80)
        ],
        help_text="The age must be between 18 and 100 years."
    )
    date_created = models.DateTimeField(auto_now_add=True)
    
    # def user_upload_to(instance, filename):
    #     return f'users/{instance.user.username}/{filename}'

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user = instance
        )
    else:
        pass