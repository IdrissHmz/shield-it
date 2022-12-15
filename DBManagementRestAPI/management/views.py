from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from management.models import UserProfile
from management.models import Email
from management.serializers import UserSerializer
from management.serializers import EmailSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def user_list(request):
    # GET list of users, POST a new user, DELETE all users
    if request.method == 'GET':
        users = UserProfile.objects.all()
        
        email = request.GET.get('email', None)
        if email is not None:
            users = users.filter(email__icontains=email)
        
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = UserProfile.objects.all().delete()
        return JsonResponse({'message': '{} users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    # find user by pk (id)
    try: 
        user = UserProfile.objects.get(pk=pk) 
        if request.method == 'GET': 
            user_serializer = UserSerializer(user) 
            return JsonResponse(user_serializer.data)
        elif request.method == 'PUT': 
            user_data = JSONParser().parse(request) 
            user_serializer = UserSerializer(user, data=user_data) 
            if user_serializer.is_valid(): 
                user_serializer.save() 
                return JsonResponse(user_serializer.data) 
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        elif request.method == 'DELETE': 
            user.delete() 
            return JsonResponse({'message': 'user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    
    except UserProfile.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

    
        
#############################################################################################################################""



@api_view(['GET', 'POST', 'DELETE'])
def mail_list(request):
    # GET list of users, POST a new user, DELETE all users
    if request.method == 'GET':
        users = Email.objects.all()
        
        email = request.GET.get('email', None)
        if email is not None:
            users = users.filter(email__icontains=email)
        
        users_serializer = EmailSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
        # 'safe=False' for objects serialization
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = EmailSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        count = Email.objects.all().delete()
        return JsonResponse({'message': '{} users were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def mail_detail(request, pk):
    # find user by pk (id)
    try: 
        user = Email.objects.get(pk=pk) 
        if request.method == 'GET': 
            user_serializer = EmailSerializer(user) 
            return JsonResponse(user_serializer.data)
        elif request.method == 'PUT': 
            user_data = JSONParser().parse(request) 
            user_serializer = EmailSerializer(user, data=user_data) 
            if user_serializer.is_valid(): 
                user_serializer.save() 
                return JsonResponse(user_serializer.data) 
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        elif request.method == 'DELETE': 
            user.delete() 
            return JsonResponse({'message': 'user was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)    
    except Email.DoesNotExist: 
        return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 

@api_view(['GET'])
def user_mails(request,pk):
    print(pk)
    emails = Email.objects.all()
    #emails = Email.objects.filter(employee=int(pk))
    #emails = emails.filter(lambda x: x['employee']==pk)
    emails = [x for x in emails if x.employee==int(pk)]
    print(emails)
    if request.method == 'GET': 
        emails_serializer = EmailSerializer(emails, many=True)
        return JsonResponse(emails_serializer.data, safe=False)