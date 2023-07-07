from rest_framework.decorators import api_view
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



from .serializers import TodoSerializer
from .models import TodoList
# Create your views here.
@api_view()
def home(request):
  todo = TodoList.objects.all()
  serializer = TodoSerializer(todo,many=True)
  return Response({
    "message":"Success",
    "data":serializer.data
  })
  
@api_view(["POST"])
def add_todo(request):
  try:
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
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
def delete_todo(request,id=None):
  try:
    if id:
      try:
        todo = TodoList.objects.get(id=id)
        todo.delete()
        return Response({
          'message':'Successfully Deleted'
          },status=HTTP_204_NO_CONTENT)
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