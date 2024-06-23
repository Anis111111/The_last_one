# Generated by Django 4.2.13 on 2024-06-23 12:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.IntegerField(auto_created=True, default=0, primary_key=True, serialize=False)),
                ('reset_password_token', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('reset_password_expire', models.DateTimeField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, height_field='height', null=True, upload_to='photos/', width_field='width')),
                ('phone', models.CharField(max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone', message='The phone must be 10 numbers long.', regex='^\\d{10}$')])),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('age', models.PositiveIntegerField(default=19, help_text='The age must be between 18 and 100 years.', validators=[django.core.validators.MinValueValidator(19), django.core.validators.MaxValueValidator(80)])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]