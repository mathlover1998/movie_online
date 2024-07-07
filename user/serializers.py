from rest_framework import serializers
from movie_app.models import *
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(trim_whitespace=True,required=True,write_only=True)
    class Meta:
        model = User
        fields = ('email','password','re_password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_password(self,value):
        re_password = self.initial_data.get('re_password')
        if value != re_password:
            raise serializers.ValidationError("Both Password must be the same")
        return value

    def validate(self, attrs):
        if not all(attrs.values()):
            raise serializers.ValidationError("Must provide all fields")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('re_password', None)
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self,attrs):
        if all(attrs.values()):
            user = authenticate(request=self.context.get('request'),email=attrs['email'],password =attrs['password'])
            if user:
                attrs['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
            return attrs
        else:
            return serializers.ValidationError("Must provide all fields")


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    re_password = serializers.CharField()
    class Meta:
        # fields = ('password','new_password','re_password')
        extra_kwargs = {'password': {'write_only': True,'style':{'input_type': 'password'}},
                        'new_password': {'write_only': True,'style':{'input_type': 'password'}},
                        're_password': {'write_only': True,'style':{'input_type': 'password'}}}


    def validate(self, attrs):
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        re_password = attrs.get('re_password')
        user = self.context['request'].user

        if not check_password(password, user.password):
            raise serializers.ValidationError('Invalid old password')

        if password == new_password:
            raise serializers.ValidationError('New password must be different than old password')

        if new_password != re_password:
            raise serializers.ValidationError('Both new passwords must match')
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','email','name','user_image')
        read_only_fields = ('email',)
        
class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(required=False)
    email = serializers.EmailField(source='user.email',required=False)
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('info','first_name','last_name','display_name','email','phone_number','full_name')
        read_only_fields = ('email','phone_number')
        extra_kwargs = {'first_name': {'write_only':True},'last_name': {'write_only':True}}

    def get_full_name(self,obj):
        return obj.full_name
    
    def validate(self, attrs):
        if Profile.objects.filter(display_name = attrs.get('display_name')).exists():
            raise serializers.ValidationError('Display must be unique')
        return attrs
    
    def update(self,instance, validated_data):
        instance.info = validated_data.get('info', instance.info)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.display_name = validated_data.get('display_name', instance.display_name)
        instance.save()
        return validated_data

class PhoneNumberSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField(max_length=15)
    
class OTPVerificationSerializer(serializers.Serializer):
    new_phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)