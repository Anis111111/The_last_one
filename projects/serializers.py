from rest_framework import serializers
from .models import Project, Review


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

        
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Review
        fields = "__all__"
