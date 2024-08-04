from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required
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
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/accounts/profile')  
        else:
            error_message = form.errors.as_text()
            return render(request , 'register.html',{'error':error_message} )      
    else:
        form = SignupForm()
    return render(request , 'registration/signup.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get['email']
        password = request.POST.get['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accounts/profile')
        else:
            return render(request , 'login.html',{'error':'Invalid credentials. Please try again.'} )      

    return redirect('/accounts/profile')  

@login_required
@permission_classes([IsAuthenticated])
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request , 'profile/profile.html',{'profile':profile})

@login_required
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