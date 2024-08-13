from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal

from professors.models import Professor
from accounts.models import Profile
# تعريف إشارة جديدة
professor_created = Signal()

@receiver(professor_created)
def create_professor(sender, **kwargs):
    profile = kwargs['profile']
    # إنشاء كائن Professor جديد
    Professor.objects.create(profile=profile)