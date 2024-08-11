from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Profile
from professors.models import Professor
from students.models import Student

class SingUpSerializer(serializers.ModelSerializer): 
    type_Professor = serializers.BooleanField(required=True)
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password','type_Professor')

        extra_kwargs = {
            'first_name' : {'required':True , 'allow_blank':False},
            'last_name' : {'required':True , 'allow_blank':False},
            'email' : {'required':True , 'allow_blank':False},
            'password' : {'required':True , 'allow_blank':False,'min_length':8}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', 'username')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        exclude = ('profile',)

class ProfileProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile = ProfileSerializer()
    professor = ProfessorSerializer()

    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Profile
        fields = ('user','user_id', 'profile', 'professor')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        professor_data = validated_data.pop('professor', {})
        
        # Update Profile
        for attr, value in profile_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update Professor
        professor = instance.professor
        for attr, value in professor_data.items():
            setattr(professor, attr, value)
        professor.save()
        
        return instance
        
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        professor_data = validated_data.pop('professor')

        user = self.context['request'].user
        profile = Profile.objects.create(user=user, **profile_data)
        Professor.objects.create(profile=profile, **professor_data)
        
        return profile


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ('profile',)

class ProfileStudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile = ProfileSerializer()
    student = StudentSerializer()

    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Profile
        fields = ('user_id', 'user', 'profile', 'student')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        student_data = validated_data.pop('student')
        
        user = self.context['request'].user
        profile = Profile.objects.create(user=user, **profile_data)
        Student.objects.create(profile=profile, **student_data)
        
        return profile

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        student_data = validated_data.pop('student', {})
        
        # Update Profile
        for attr, value in profile_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update student
        student = instance.student
        for attr, value in student_data.items():
            setattr(student, attr, value)
        student.save()
        
        return instance