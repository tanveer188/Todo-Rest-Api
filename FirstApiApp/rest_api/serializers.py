from rest_framework import serializers
from .models import TodoList
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList 
        fields = '__all__'
    def validate_title(self,data):
      if len(data) <= 5 :
        raise serializers.ValidationError("title mus contain at least 5 characters")
      return data
        
