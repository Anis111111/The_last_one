from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class SingUpSerializer(serializers.ModelSerializer): # UserSerializer
    class Meta:
        model = User
        fields = ('first_name','last_name','email','password')

        extra_kwargs = {
            'first_name' : {'required':True , 'allow_blank':False},
            'last_name' : {'required':True , 'allow_blank':False},
            'email' : {'required':True , 'allow_blank':False},
            'password' : {'required':True , 'allow_blank':False,'min_length':8}
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"