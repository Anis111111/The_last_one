from django.contrib.auth import authenticate , login
from django.shortcuts import render , redirect

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view , permission_classes

from .serializers import SingUpSerializer 
from .forms import SignupForm , UserForm , ProfileForm
from .models import Profile

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username ,password=password)
            login(request,user)
            return redirect('/accounts/profile')        
    else:
        form = SignupForm()
    return render(request , 'registration/signup.html',{'form':form})

@permission_classes([IsAuthenticated])
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request , 'profile/profile.html',{'profile':profile})

@permission_classes([IsAuthenticated])
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userform = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST,instance=profile)
        if userform.is_valid() and profile_form.is_valid():
            userform.save()
            myform = profile_form.save(commit=False)
            myform.user = request.user
            myform.save()
            return redirect('/accounts/profile')
    else:
        userform = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)


    return render(request , 'profile/profile_edit.html',{
        'userform' : userform ,
        'profileform' : profile_form,
    })