# Generated by Django 4.2.13 on 2024-07-04 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField()),
                ('project_type', models.CharField(choices=[('web', 'Web'), ('desktop', 'Desktop Program'), ('ai', 'AI Program'), ('full_stack', 'Full Stack App'), ('mobile', 'Mobile App')], default='web', max_length=20, verbose_name='project type')),
                ('status', models.CharField(choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('done', 'Done'), ('backlog', 'Backlog')], default='backlog', max_length=20, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='', max_length=1000)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='projects.project')),
            ],
        ),
    ]
