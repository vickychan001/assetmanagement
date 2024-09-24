from rest_framework import serializers
from .models import CustomUser, Assets
from django.contrib.auth import authenticate

class ManagerRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def create(self, data):
        user = CustomUser(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            is_staff=True
        )
        user.set_password(data.get('password'))  # Hash the password
        user.save()
        return user

class EmployeeRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, data):
        user = CustomUser(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username:
            raise serializers.ValidationError({"username": "This field is required."})
        
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"message": "Invalid credentials."})

        attrs['user'] = user
        return attrs


class AddAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'

class AssetAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'asset_assigned']
    
    def validate_id(self, value):
        user = CustomUser.objects.filter(id=value)
        if user.exists():
            return value
        else:
            raise serializers.ValidationError({"Invalid ID": "The provided ID does not exist."})
    
    def update(self, instance, validated_data):
        instance.asset_assigned = validated_data.get('asset_assigned', instance.asset_assigned)
        instance.save()
        return instance