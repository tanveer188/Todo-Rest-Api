from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import TodoList
from django.contrib.auth.models import User
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList 
        exclude = ("user",)
    def validate_title(self,data):
      if len(data) <= 5 :
        raise serializers.ValidationError("title mus contain at least 5 characters")
      return data
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username","password")
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if len(username) < 6 or len(username) > 16:
            raise serializers.ValidationError({"username": "Username must be between 6 and 16 characters long."})
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least 1 digit."})
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least 1 letter."})
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
        
class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if len(username) < 6 or len(username) > 16:
            raise serializers.ValidationError({"username": "Username must be between 6 and 16 characters long."})
        if len(password) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least 1 digit."})
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError({"password": "Password must contain at least 1 letter."})
        return data