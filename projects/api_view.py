from django.shortcuts import render , get_object_or_404

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework import status

from .serializers import ProjectSerializer , ReviewSerializer
from .filters import ProjectFilter
from .models import *

from django.db.models import Avg



# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_projects(request):
    # project = Project.objects.all() # for delete
    filterset = ProjectFilter(request.GET , queryset=Project.objects.all().order_by('id'))

    count = filterset.qs.count()
    resPage = 10
    paginator = PageNumberPagination()
    paginator.page_size = resPage

    queryset = paginator.paginate_queryset(filterset.qs,request)

    # serializer = ProjectSerializer(project , many = True) # for delete
    serializer = ProjectSerializer(queryset , many = True , context={"request":request} )
    # print(project) # for delete
    
    return Response({"project":serializer.data, "per page": resPage , "count":count})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_id(request,pk):

    project =get_object_or_404(Project , id = pk)
    serializer = ProjectSerializer(project , many = False , context={"request":request} )
    print(project)
    return Response({"project":serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_project(request):

    data = request.data
    serializer = ProjectSerializer(data = data)

    if serializer.is_valid():
        project = Project.objects.create(**data,user = request.user)
        res = ProjectSerializer(project , many = False , context={"request":request})
        return Response({"project":res.data})
    else:
        return Response(serializer.errors)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_project(request , pk):

    project = get_object_or_404(Project , id = pk)
    
    if project.user != request.user :
        return Response(
                        {"error":"Sorry you can not update this project"},
                        status = status.HTTP_403_FORBIDDEN
                        )
    
    project.title = request.data['title']
    project.description = request.data['description']
    project.project_type = request.data['project_type']
    project.is_published = request.data['is_published']
    project.updated_at = request.data['updated_at']
    project.status = request.data['status']
    project.created_at = request.data['created_at']

    project.save()

    serializer = ProjectSerializer(project , many = False , context={"request":request})
    return Response({"project":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_project(request , pk):

    project = get_object_or_404(Project , id = pk)
    
    if project.user != request.user :
        return Response(
                        {"error":"Sorry you can not DELETE this project"},
                        status=status.HTTP_403_FORBIDDEN
                        )

    project.delete()
    return Response(
                    {"details":"Delete action is done!!"},
                    status=status.HTTP_200_OK
                    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request,pk):

    project =get_object_or_404(Project,id = pk)
    data = request.data
    user = request.user
    review = project.reviews.filter(user = user)

    if data['rating'] <= 0 or data['rating'] > 10 :
        return Response(
                        {"error":"Please select between 1 to 10 only"},
                        status=status.HTTP_400_BAD_REQUEST
                        )
    elif review.exists():
        new_review ={'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)

        rating = project.reviews.aggregate(avg_ratings = Avg('rating'))
        project.ratings = rating['avg_ratings']
        project.save()

        return Response({'details':'Project review updated !!!' })
    else:
        Review.objects.create(
            user = user,
            project = project,
            rating = data['rating'],
            comment = data['comment']
        )

        rating = project.reviews.aggregate(avg_ratings = Avg('rating'))
        project.ratings = rating['avg_ratings']
        project.save()

        return Response({'details':'Project review created ...' })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):

    user = request.user
    project =get_object_or_404(Project,id = pk)
    
    review = project.reviews.filter(user = user)

    if review.exists() :
        review.delete()
        rating = project.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            project.ratings = rating['avg_ratings'] 
            project.save()
            return Response({"details":"Project review Deleted !!!"})

    else:
        return Response(
                        {"error":"Review NOT found!!"},
                        status=status.HTTP_404_NOT_FOUND
                        )

