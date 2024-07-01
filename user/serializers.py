from rest_framework import serializers
from movie_app.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password

class RegisterSerializer(serializers.ModelSerializer):
    
    re_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email','name','password','re_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        re_password = attrs.get('re_password')
        if all([email, password, re_password]):
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email must be unique")
            if password != re_password:
                raise serializers.ValidationError("Both Password must be the same")
            else:
                return attrs
        raise serializers.ValidationError("Must provide all fields")    
    def create(self, validated_data):
        validated_data.pop('re_password', None)
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True,'style':{'input_type': 'password'}}}

    def validate(self, data):
        email = data['email']
        password = data['password']

        if email and password:
            user = authenticate(request= self.context.get('request'),email=email,password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is disabled")
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return data

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    re_password = serializers.CharField()
    class Meta:
        fields = ('password','new_password','re_password')
        extra_kwargs = {'password': {'write_only': True,'style':{'input_type': 'password'}},
                        'new_password': {'write_only': True,'style':{'input_type': 'password'}},
                        're_password': {'write_only': True,'style':{'input_type': 'password'}}}
    
    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        re_password = attrs.get('re_password')
        user = self.context.get('user')

        if password and check_password(password,user.password):
            if new_password == re_password:
                user.set_password(new_password)
                user.save()
                return attrs
            raise serializers.ValidationError("Both password must be the same")
        raise serializers.ValidationError("Your old password is not correct")

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ('image','is_main_image')

class UserSerializer(serializers.ModelSerializer):
    user_image = UserImageSerializer(required=False)
    class Meta:
        model = User
        fields = ('id','email','name','user_image')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        user_image_data = validated_data.pop('user_image',None)
        if user_image_data:
            user_image = instance.user_image
            if user_image:
                user_image_serializer = UserImageSerializer(user_image,data=user_image_data,partial=True)
                if user_image_serializer.is_valid():
                    user_image_serializer.save()
        return super().update(instance, validated_data)
