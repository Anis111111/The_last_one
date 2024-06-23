from django.db import models
from accounts.models import Profile
from professors.models import Professor 


class Project(models.Model):

    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('backlog', 'Backlog'),
    )
    TYPE_CHOICES = (
        ('web', 'Web'),
        ('desktop', 'Desktop Program'),
        ('ai', 'AI Program'),
        ('full_stack', 'Full Stack App'),
        ('mobile', 'Mobile App'),
    )

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    idea = models.TextField(unique=True)

    # add project type
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='web', verbose_name='project type')

    # add status for project
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='backlog', verbose_name='status')

    is_published = models.BooleanField(default=False, verbose_name='Is Published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        


class Review(models.Model):
    # user = models.ForeignKey(User , null = True , on_delete = models.SET_NULL)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, db_index=True)

    project = models.ForeignKey(Project , null = True , on_delete = models.CASCADE , related_name = 'reviews')

    comment = models.TextField(max_length = 1000 , default = "" , blank = False)
    createAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.comment

