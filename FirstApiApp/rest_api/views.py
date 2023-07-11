from rest_framework.decorators import api_view

#auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
#response
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)
#decorator serilizer models
from django.views.decorators.csrf import csrf_exempt


from .serializers import TodoSerializer,UserSerializer
from .models import TodoList
# Create your views here.
@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def home(request):
  todo = TodoList.objects.filter(user=request.user)
  serializer = TodoSerializer(todo,many=True)
  return Response({
    "message":"Success",
    "data":serializer.data
  },status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated, ))
def add_todo(request):
  try:
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
      todo_obj = serializer.save(user=request.user)
      return Response({
        "message":"Successfully Saved",
        "data":serializer.data
      },status=HTTP_201_CREATED)
    return Response({
      "message":"Invalid Data",
      "data":serializer.errors
    },status=HTTP_400_BAD_REQUEST)
  except Exception as e:
    print(e)
  return Response({
  'message':'something went wrong'
  },status=HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@permission_classes((IsAuthenticated, ))
def delete_todo(request,id=None):
  try:
    if id:
      try:
        todo = TodoList.objects.get(id=id)
        if todo.user == request.user:
            todo.delete()
            return Response({
              'message':'Successfully Deleted'
              },status=HTTP_204_NO_CONTENT)
        else:
            return Response({
              'message':'Wrong Request'
              },status=HTTP_400_BAD_REQUEST)
      except Exception as e:
        print(e)
        return Response({
          'message':'Todo Not Found'
          },status=HTTP_404_NOT_FOUND)
      else:
        return Response({
          'message':'id is required'
          },status=HTTP_400_BAD_REQUEST)
  except Exception as e:
    print(e)
  return Response({
  'message':'something went wrong'
  },status=HTTP_500_INTERNAL_SERVER_ERROR)
  
  
@api_view(["PATCH"])
@permission_classes((IsAuthenticated, ))
def done(request,pk):
  try:
    if pk:
      try:
        todo = TodoList.objects.get(id=pk)
        if todo.user == request.user:
            todo.is_done = True
            todo.save()
            serializer = TodoSerializer(todo)
            return Response({
              "message":"Sccessfully Updated",
              "data":serializer.data
              },status=HTTP_204_NO_CONTENT)
        else:
            return Response({
              'message':'Wrong Request'
              },status=HTTP_400_BAD_REQUEST)
      except Exception as e:
        print(e)
        return Response({
          'message':'Todo Not Found'
          },status=HTTP_404_NOT_FOUND)
      else:
        return Response({
          'message':'id is required'
          },status=HTTP_400_BAD_REQUEST)
  except Exception as e:
    print(e)
  return Response({
  'message':'something went wrong'
  },status=HTTP_500_INTERNAL_SERVER_ERROR)
 
  
@api_view(["POST"])
def signup(request):
  try:
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response({
      "message":"Sccessfully Account Created",
      },status=HTTP_201_CREATED)
    else:
      return Response({
      "message":"Invalid Credinatials",
      "data":serializer.errors
      })
  except:
    return Response({
    "message":"something went wrong",
    },status=HTTP_500_INTERNAL_SERVER_ERROR)
      
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
@api_view(["POST"])
def login(request):
  try:
    data = request.data
    username = data.get("username")
    password = data.get("password")
    print(username,password)
    user = authenticate(request._request,username = username,password = password)
    if user is not None:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        },status=HTTP_200_OK)
    else:
      try:
        User.objects.get(username=username)
        return Response({
        "message":"Login Failed",
        "data":{
          "password":["Incorrect Password"]
        }
        },status=HTTP_200_OK)
      except:
        return Response({
        "message":"Login Failed",
        "data":{
          "username":["Incorrect username"]
        }
        },status=HTTP_200_OK)
  except:
    return Response({
    "message":"something went wrong",
    },status=HTTP_500_INTERNAL_SERVER_ERROR)
      