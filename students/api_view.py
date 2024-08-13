from django.shortcuts import render,get_object_or_404

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated , IsAdminUser , AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import status

from .filters import StudentFilter
from .models import *
from .serializers import StudentSerializer ,StudentGroupSerializer
from .permissions import ReadOnly ,IsOwnerOrReadOnly

from django.db.models import Avg



# Create your views here.
class StudentsAPIList(ListAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})

class StudentGroupAPICreateList(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [IsAuthenticated,]    
    
    def create(self, request, *args, **kwargs):
        request.user.is_admin = True  
        request.user.save()

        serializer = self.get_serializer(data=request.data)  
        serializer.is_valid(raise_exception=True)  
        self.perform_create(serializer)  
        return Response(serializer.data, status=status.HTTP_201_CREATED) 

    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})
        
class StudentGroupAPIRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = StudentGroup.objects.all()
    serializer_class = StudentGroupSerializer
    permission_classes = [AllowAny]    
    
    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})

class StudentAPIDetail(RetrieveAPIView):
    authentication_classes = (TokenAuthentication)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})
        
class StudentAPIUpdate(UpdateAPIView):
    authentication_classes = (TokenAuthentication)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})

class StudentAPIDestroy(DestroyAPIView):
    authentication_classes = (TokenAuthentication)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def is_secure_Q(request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"details": "User is authenticated and logged in."})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_all_students(request):

#     filterset = StudentFilter(request.GET,queryset=Student.objects.all().order_by('id'))

#     count = filterset.qs.count()
#     resPage = 10
#     paginator = PageNumberPagination()
#     paginator.page_size = resPage

#     queryset = paginator.paginate_queryset(filterset.qs , request)

#     serializer = StudentSerializer(queryset , many = True, context={"request":request})

#     return Response({"student":serializer.data , "per page": resPage , "count":count})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_by_id(request,pk):
    
#     student =get_object_or_404(Student , id = pk)
#     serializer = StudentSerializer(student , many = False, context={"request":request})
#     print(student)
#     return Response({"student":serializer.data})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def new_student(request):

#     data = request.data
#     serializer = StudentSerializer(data = data)

#     if serializer.is_valid():
#         student = Student.objects.create(**data , user = request.user)
#         res = StudentSerializer(student , many = False, context={"request":request})
#         return Response({"student":res.data})
#     else:
#         return Response(serializer.errors)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_student(request , pk):

#     student = get_object_or_404(Student , id = pk)
    
#     if student.user != request.user :
#         return Response(
#                         {"error":"Sorry you can not update this student"},
#                         status = status.HTTP_403_FORBIDDEN
#                         )
    
#     student.profile = request.data['profile']
#     student.university_id = request.data['university_id']
#     student.specialization = request.data['specialization']
#     student.group = request.data['group']
#     student.save()

#     serializer = StudentSerializer(student , many = False, context={"request":request})
#     return Response({"student":serializer.data})


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated , IsAdminUser])
# def delete_student(request , pk):

#     student = get_object_or_404(Student , id = pk)
    
#     if student.user != request.user :
#         return Response(
#                         {"error":"Sorry you can not DELETE this student"},
#                         status = status.HTTP_403_FORBIDDEN
#                         )

#     student.delete()
#     return Response(
#                     {"details":"Delete action is done!!"},
#                     status = status.HTTP_200_OK
#                     )
