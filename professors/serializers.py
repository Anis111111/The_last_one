from rest_framework import serializers
from .models import Professor
from accounts.models import Profile

class ProfessorSerializer(serializers.ModelSerializer):
    profile = serializers.ChoiceField(choices=[(profile.id, profile.user.username) for profile in Profile.objects.all()] + [('other', 'Other')])

    class Meta:
        model = Professor   
        fields = '__all__'