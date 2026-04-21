from rest_framework import serializers
from accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'fullname', 'phone_number', 'type', 'lang', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'fullname', 'phone_number', 'type', 'lang', 'status']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'fullname',
            'email',
            'phone_number',
            'type',
            'lang',
            'status',
            'created_at',
        ]



class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'phone_number', 'image', 'type']
        read_only_fields = ['id', 'email', 'type']


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname', 'phone_number', 'image', 'type']
        read_only_fields = ['id', 'email', 'type']


