from django.db import models
from accounts.models import Profile
from projects.models import Project
from professors.models import Professor
from django.core.exceptions import ValidationError
import importlib


def get_student_model():
    students_models = importlib.import_module('students.models')
    return students_models.Student

class StudentGroup(models.Model):
    # Every Group must have many student and one professor
    id = models.AutoField(primary_key=True) 
    project_idea = models.OneToOneField('projects.Project', on_delete=models.CASCADE )
    admin = models.ForeignKey('professors.Professor', on_delete=models.CASCADE, related_name='admin_groups' )
    is_published = models.BooleanField(default=False, verbose_name='Is Published', editable=False )

    @property
    def students_count(self):
        return self.students.count()

    def __str__(self):
        return f"Group {self.id}"

    def get_students(self):
        return get_student_model().objects.filter(project=self)

    # Check only if the model already exists.
    def save(self, *args, **kwargs):
        if hasattr(self, 'students'):
            student_count = self.students.count()
            if student_count < 2 or student_count > 6:
                raise ValidationError('The number of students must be between 2 and 6.')
        super(StudentGroup, self).save(*args, **kwargs)

    # Ensure the basic validation is executed.
    def clean(self):
        if hasattr(self, 'students'):
            student_count = self.students.count()
            if student_count < 2 or student_count > 6:
                raise ValidationError('The number of students must be between 2 and 6.')

    def delete(self, *args, **kwargs):
        user = kwargs.get('user')
        if user and user.profile != self.admin.profile:
            raise PermissionError("You do not have permission to delete this group.")
        super(StudentGroup, self).delete(*args, **kwargs)

    # Additional acceptance logic here
    def accept(self, *args, **kwargs):
        # Acceptance logic here
        user = kwargs.get('user')
        if user and user.profile != self.admin.profile:
            self.is_published = True
            self.save()

class Student(models.Model):
    SPECIALIZATIONS = (
        ('networks', 'networks'),
        ('software', 'software'),
    ) 
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    university_id = models.CharField(max_length=20, unique=True)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='student', blank=True, null=True )
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS, default='software', verbose_name='specialization')

    def __str__(self):
        return self.profile.user.username