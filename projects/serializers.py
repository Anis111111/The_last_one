from rest_framework import serializers

from students.serializers import StudentSerializer

from .models import Project, Review



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

        
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Review
        fields = "__all__"

class ProjectDetailSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'students']  # أضف الحقول التي تحتاجها