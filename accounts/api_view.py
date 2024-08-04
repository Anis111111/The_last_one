from django.shortcuts import render , get_object_or_404 , redirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth import authenticate , login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework import status 

from dj_rest_auth.views import LogoutView ,LoginView 

from datetime import datetime , timedelta

from .models import Profile
from .serializers import ProfileSerializer , SingUpSerializer 


class register(CreateAPIView):
    serializer_class = SingUpSerializer

    def create(self, request, *args, **kwargs):
        user = SingUpSerializer(data=request.data)
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if user.is_valid():
                if not User.objects.filter(username=data["email"]).exists():
                    user = User.objects.create(
                        username = data["email"],
                        first_name = data["first_name"],
                        last_name = data["last_name"],
                        email = data["email"],
                        password = make_password(data["password"]),
                        type = data["type"],
                    )
                    return Response(
                                    {"details": "Your account registered successfully !",'redirect_url': '/api/profile/'},
                                    status=status.HTTP_201_CREATED,
                                    )
                else:
                    return Response(
                                    {"error": "This email already exists!"},
                                    status=status.HTTP_400_BAD_REQUEST,
                                    )
            else:
                return Response(user.errors)
        else:
            form = SignupForm()


class LoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({
                "detail": "Successfully, You are here Hi there :D",
                'redirect_url': '/api/dashboard',
                'token': token.key 
                }, status=status.HTTP_200_OK)
        
        # if the login is falut then return the origin response
        return response


# @api_view(["POST",])
# def logout_user(request):
#     if request.method == "POST":
#         request.user.auth_token.delete()
#         return Response({"Message":"You are logged out!!!"},status=status.HTTP_200_OK)

class LogoutView(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
        
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
            
            return Response({"detail": "You are logged out !!", 'redirect_url': '/api/login/'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "there is an error #_#"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = SingUpSerializer(request.user, many=False, context={"request":request})
    return Response(user.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data["first_name"]
    user.username = data["email"]
    user.last_name = data["last_name"]
    user.email = data["email"]

    if data["password"] != "":
        user.password = make_password(data["password"])

    user.save()
    serializer = SingUpSerializer(user, many=False, context={"request":request})
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    project = get_object_or_404(Project, id=pk)

    review = project.reviews.filter(user=user)

    if review.exists():
        review.delete()
        rating = project.reviews.aggregate(avg_ratings=Avg("rating"))
        if rating["avg_ratings"] is None:
            rating["avg_ratings"] = 0
            project.ratings = rating["avg_ratings"]
            project.save()
            return Response({"details": "Project review Deleted !!!"})
    else:
        return Response(
                        {"error": "Review NOT found!!"}, 
                        status=status.HTTP_404_NOT_FOUND
                        )


@api_view(["POST"])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User, email=data["email"])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    host = get_current_host(request)

    # http://localhost:8000/ or {host}
    link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "password reset from eProject", body, "eProject@gmail.com", [data["email"]]
    )
    return Response({"details": "password reset sent to {email}".format(email=data["email"])})


@api_view(["POST"])
def reset_password(request, token):

    data = request.data
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response(
            {"error": "Token is expired"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if data["password"] != data["confirmPassword"]:
        return Response(
                        {"error": "password are not same"},
                        status=status.HTTP_400_BAD_REQUEST
                        )

    user.password = make_password(data["password"])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()

    user.save()

    return Response({"details": "password reset done"})
