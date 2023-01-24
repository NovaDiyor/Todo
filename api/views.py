from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@api_view(['POST'])
def login_view(request):
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            usr = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'username': username,
                    'user_id': usr.id,
                    'token': token.key,
                }
                return Response(data, status.HTTP_200_OK)
            else:
                message = 'Username or Password is wrong!'
                data = {
                    'message': message,
                }
                return Response(data, status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            message = {
                'message': 'This User Doesnt Exist'
            }
            return Response(message, status.HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": f'{err}'})


@api_view(['POST'])
def register(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            name = request.POST['name']
            password = request.POST['password']
            if len(password) >= 6:
                usr = User.objects.create_user(username=username, first_name=name, password=password, status=2)
                token = Token.objects.create(user=usr)
                data = {
                    'username': username,
                    'name': name,
                    'user_id': usr.id,
                    'token': token.key
                    }
                return Response(data, status.HTTP_200_OK)
            else:
                return Response('Password have to consist of 6 letter', status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response({"error": f'{err}'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    try:
        if request.method == 'DELETE':
            user = request.user
            Token.objects.get(user=user).delete()
            logout(request)
            return Response('You logged out')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_task(request, pk):
    try:
        if request.method == 'DELETE':
            user = request.user
            task = Task.objects.get(id=pk)
            if user == task.user:
                task.delete()
                return Response('You Deleted Task', status.HTTP_202_ACCEPTED)
            else:
                return Response('You cant delete strange task', status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}', status.HTTP_417_EXPECTATION_FAILED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_task(request):
    try:
        if request.method == 'GET':
            user = request.user
            task = Task.objects.filter(user=user)
            return Response(TaskOne(task, many=True).data, status.HTTP_200_OK)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error:{err}')


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def edit_task(request, pk):
    try:
        if request.method == 'PATCH':
            user = request.user
            task = Task.objects.get(id=pk)
            title = request.POST.get('title')
            text = request.POST.get('description')
            completed = request.POST.get('completed')
            if user == task.user:
                if title:
                    task.title = title
                if text:
                    task.text = text
                if completed == 'True':
                    task.completed = True
                elif completed == 'False':
                    task.completed = False
                task.save()
                return Response('edited', status.HTTP_202_ACCEPTED)
            else:
                return Response('wrong user', status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_task(request):
    try:
        if request.method == 'POST':
            user = request.user
            title = request.POST['title']
            text = request.POST['description']
            Task.objects.create(user=user, title=title, text=text, completed=False)
            return Response('task created', status.HTTP_200_OK)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}', status.HTTP_417_EXPECTATION_FAILED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def edit_profile(request):
    try:
        if request.method == 'PATCH':
            user = request.user
            name = request.POST.get('name')
            username = request.POST.get('username')
            password = request.POST.get('password')
            img = request.FILES.get('image')
            if name:
                user.first_name = name
            if username:
                user.username = username
            if password:
                if len(password) >= 6:
                    user.password = password
                else:
                    return Response('Password have to consist of 6 letter', status.HTTP_401_UNAUTHORIZED)
            if img:
                user.img = img
            user.save()
            return Response('Successful', status.HTTP_200_OK)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}', status.HTTP_417_EXPECTATION_FAILED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_one(request, pk):
    try:
        if request.method == 'GET':
            user = request.user
            task = Task.objects.get(id=pk)
            if user == task.user:
                return Response(TaskOne(task).data)
            else:
                return Response('wrong user', status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}', status.HTTP_417_EXPECTATION_FAILED)
