from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.generics import ListCreateAPIView , RetrieveUpdateDestroyAPIView 
from rest_framework import status

from .filters import ProfessorFilter
from .models import *
from .serializers import ProfessorSerializer



class ProfessorsAPIList(ListCreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]


class ProfessorsAPIDetail(RetrieveUpdateDestroyAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]


# @api_view(['GET'])
# def get_all_professors(request):

#     filterset = ProfessorFilter(request.GET,queryset=Professor.objects.all().order_by('id'))

#     count = filterset.qs.count()
#     resPage = 10
#     paginator = PageNumberPagination()
#     paginator.page_size = resPage

#     queryset = paginator.paginate_queryset(filterset.qs , request)

#     serializer = ProfessorSerializer(queryset , many = True)

#     return Response({"Professor":serializer.data , "per page": resPage , "count":count})


# @api_view(['GET'])
# def get_by_id(request,pk):

#     professor = get_object_or_404(Professor , id = pk)
#     serializer = ProfessorSerializer(professor , many = False)
#     print(professor)
#     return Response({"professor":serializer.data})


# @api_view(['POST'])
# @permission_classes([IsAuthenticated , IsAdminUser])
# def new_professor(request):
    
#     data = request.data
#     serializer = ProfessorSerializer(data = data)

#     if serializer.is_valid():
#         professor = Professor.objects.create(**data , user = request.user)
#         res = ProfessorSerializer(professor , many = False)
#         return Response({"professor":res.data})
#     else:
#         return Response(serializer.errors)


# @api_view(['PUT'])
# @permission_classes([IsAuthenticated , IsAdminUser])
# def update_professor(request , pk):

#     professor = get_object_or_404(Professor , id = pk)
    
#     if professor.user != request.user :
#         return Response(
#                         {"error":"Sorry you can not update this Professor"},
#                         status = status.HTTP_403_FORBIDDEN
#                         )
    
#     professor.profile = request.data['profile']
#     professor.department = request.data['department']   
#     professor.phd_certificate = request.data['phd_certificate']
#     professor.phd_date = request.data['phd_date']
#     professor.specialization = request.data['specialization']
#     professor.keyword = request.data['keyword']

#     professor.save()

#     serializer = ProfessorSerializer(student , many = False)
#     return Response({"professor":serializer.data})


# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated , IsAdminUser])
# def delete_professor(request , pk):

#     professor = get_object_or_404(Professor , id = pk)
    
#     if professor.user != request.user :
#         return Response(
#                         {"error":"Sorry you can not DELETE this professor"},
#                         status = status.HTTP_403_FORBIDDEN
#                         )

#     professor.delete()
#     return Response(
#                     {"details":"Delete action is done!!"},
#                     status = status.HTTP_200_OK
#                     )
