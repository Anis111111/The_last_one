from django.dispatch import receiver
from django.db.models.signals import post_save ,pre_save
from accounts.models import Profile
from projects.models import Project
from professors.models import Professor
from django.db import models
from django.core.exceptions import ValidationError
import importlib

def get_student_model():
    students_models = importlib.import_module('students.models')
    return students_models.Student

class StudentGroup(models.Model):
    # Every Group must have many students and one professor
    # name = models.CharField(max_length=128)
    project_idea = models.OneToOneField('projects.Project', on_delete=models.CASCADE )
    professors = models.ForeignKey('professors.Professor', on_delete=models.CASCADE, related_name='Master' )
    admin = models.OneToOneField('students.Student', on_delete=models.CASCADE, related_name='admin_groups' )
    is_published = models.BooleanField(default=False, verbose_name='Is Published', editable=False )
    members = models.ManyToManyField('students.Student', through="Membership")

    @property
    def students_count(self):
        return self.students.count()

    def __str__(self):
        return f"Group {self.project_idea.title}"

    def get_students(self):
        return get_student_model().objects.filter(project=self)

    # Check only if the model already exists.
    def save(self, *args, **kwargs):
        if hasattr(self, 'students'):
            student_count = self.students.count()
            if student_count < 2 or student_count > 6:
                raise ValidationError('The number of students must be between 2 and 6.')

            # تعيين الطالب كمسؤول إذا كان is_admin True
            for student in self.students.all():
                if student.is_admin and student == self.admin:
                    self.admin = student  # تعيين الطالب كمسؤول
                    break

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
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
    university_id = models.CharField(max_length=50, blank=False, null=False, unique=True)
    group = models.ForeignKey('StudentGroup', on_delete=models.CASCADE, related_name='student', blank=True, null=True ) # my error is so bad
    specialization = models.TextField(choices=SPECIALIZATIONS, default='software', verbose_name='specialization')
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.profile.user.username


class Membership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    date_joined = models.DateField()


@receiver(post_save, sender=Student)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='students')
        instance.profile.user.groups.add(group)
