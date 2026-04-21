from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from rest_framework import serializers
from accounts import models
from rest_framework.exceptions import ParseError

from accounts.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        if user.state < 0:
            raise exceptions.ParseError("username_or_password_is_incorrect")
        token = super().get_token(user)
        token['email'] = user.email
        token['type'] = user.type
        return token




class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'image', 'type', 'lang')
        read_only_fields = ('id', )

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['first_name'] = instance.first_name,
        res['last_name'] = instance.last_name,
        res['phone_number'] = instance.phone_number,
        res['image'] = instance.image,
        res['type'] = instance.type,
        res['lang'] = instance.lang
        return res


class AccountUpdateSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=255, write_only=True, required=False)
    old_password = serializers.CharField(max_length=255, write_only=True, required=False)
    image = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('id', 'first_name', 'last_name', 'image', 'new_password', 'old_password', 'lang')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['type'] = instance.type
        return res

    def update(self, instance, validated_data):
        if 'new_password' in validated_data:
            validated_data.pop('new_password')
        if 'old_password' in validated_data:
            validated_data.pop('old_password')

        return super().update(instance, validated_data)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



