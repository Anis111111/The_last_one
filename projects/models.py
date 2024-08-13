from django.contrib.postgres.fields import ArrayField
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
    FRAMWORKS = {
        'Frontend': (
        ('react','React'),
        ('angular','Angular'),
        ('vue.js','Vue.js'),
        ('svelte','Svelte'),
        ('bootstrap','Bootstrap'),
        ),

        'Backend': (
        ('django','Django'),
        ('node.js','Node.js'),
        ('express.js','Express.js'),
        ('ruby_on_rails','Ruby on Rails'),
        ('spring_boot','Spring Boot'),
        ),

        'Mobile Apps': (
        ('flutter','Flutter'),
        ('react_native','React Native'),
        ('ionic','Ionic'),
        ('xamarin','Xamarin'),
        ('swift_ui','SwiftUI'), 
        ),
    }

    img = models.ImageField(upload_to='photos/projects', height_field='height', width_field='width', null=True, blank=True)  # user_upload_to
    height = 5 
    width = 5 

    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField()

    # add project type this field can students change it
    project_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='web', verbose_name='project type')

    # add status for project this field can students change it
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='backlog', verbose_name='status')

    FramworksFrontend = models.CharField(max_length=20, choices=FRAMWORKS['Frontend'],default='react', blank=True,null=True, verbose_name='Frontend')
    FramworksBackend = models.CharField(max_length=20, choices=FRAMWORKS['Backend'],default='django', blank=True,null=True, verbose_name='Backend')
    FramworksMobileApps = models.CharField(max_length=20, choices=FRAMWORKS['Mobile Apps'],default='flutter', blank=True,null=True, verbose_name='Mobile Apps')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False, verbose_name='Is Published')
        
    def __str__(self):
        return self.title

class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, db_index=True)

    project = models.ForeignKey(Project , null = True , on_delete = models.CASCADE , related_name = 'reviews')

    comment = models.TextField(max_length = 1000 , default = "" , blank = False)
    createAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.comment

