from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'phone', 'name']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6)
    class Meta:
        model = User
        fields = ["id",'phone','name','password']

    def create(self, validated_data):
        user = User.objects.create(
            phone = validated_data['phone'],
            password = validated_data['password'],
            name = validated_data['name'],
        )
        

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        name = attrs.get("name")
        password = attrs.get("password")

        if password and phone:
            user = authenticate(username=phone,password=password)
            if not user:
                raise serializers.ValidationError("Неверный номер или логин")
            else: 
                raise serializers.ValidationError("Введите телефон и пароль")            
            
        attrs['user'] = user
        return attrs