from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages

from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import status

from accounts.models import Profile
from .filters import ProfessorFilter
from .models import *
from .serializers import ProfessorSerializer



class ProfessorAPIListCreate(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProfessorSerializer(queryset, many = True, context={'request':request})
        if queryset.exists():
            return Response(serializer.data, status=status.HTTP_200_OK )
        else:
            return Response({'Message':'No Professor Found'}, status=status.HTTP_404_NOT_FOUND )
    
    def create(self, request, *args, **kwargs):
        profile_id = request.data.get('profile')  
        if profile_id == 'other': 
            return Response({'message': 'Please fill out the profile form.', 'redirect_url': '/api/profiles/new/'}, status=status.HTTP_302_FOUND) # edit1 
        else:
            profile = Profile.objects.get(id=profile_id) 

        serializer = ProfessorSerializer(data=request.data, context={'request': request})  # edit3 
        serializer.is_valid(raise_exception=True)
        serializer.save(professor=self.request.user, profile=profile)  # edit4 
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context(*args, **kwargs)
        context['profiles'] = Profile.objects.all() 
        return context

    # def add_professor(request):
    #     if request.method == 'POST':
    #         profile_id = request.POST.get('profile')
        
    #         if profile_id == 'another':
    #             # الحصول على بيانات ملف التعريف الجديد
    #             username = request.POST.get('username')
    #             # هنا يمكنك إضافة حقول أخرى كما تحتاج
            
    #             # إنشاء مستخدم جديد
    #             user = User.objects.create(username=username)
    #             # إنشاء ملف تعريف جديد
    #             profile = Profile.objects.create(user=user)
    #         else:
    #             # الحصول على ملف التعريف الحالي
    #             profile = Profile.objects.get(id=profile_id)

    #         # إنشاء أستاذ جديد
    #         professor = Professor(
    #             profile=profile,
    #             department=request.POST.get('department'),
    #             phd_certificate=request.FILES.get('phd_certificate'),
    #             phd_date=request.POST.get('phd_date'),
    #             specialization=request.POST.get('specialization')
    #         )
    #         professor.save()

    #         messages.success(request, 'Professor added successfully!')
    #         # return redirect('some_view_name')  # استبدل بـ view المناسب

    #     profiles = Profile.objects.all()  # استرجاع جميع ملفات التعريف
    #     return render(request, 'add_professor.html', {'profiles': profiles})

class ProfessorAPIDetail(RetrieveAPIView):
    authentication_classes = (TokenAuthentication, )
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, ]

class ProfessorAPIUpdate(UpdateAPIView):
    authentication_classes = (TokenAuthentication, )
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, ]

class ProfessorAPIDestroy(DestroyAPIView):
    authentication_classes = (TokenAuthentication, )
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser ]
    
    
    # def get(self, request):
    #     user = request.user
    #     return Response({'message': f'Hello, {user.username}!'}, status=status.HTTP_200_OK)

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
