from rest_framework import serializers
from .models import Gym, Location, SportType
from accounts.models import User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address']


class SportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportType
        fields = ['id', 'name']



class GymSerializer(serializers.ModelSerializer):
    """Serializer for Gym model"""
    class Meta:
        model = Gym
        fields = [
            'id', 'name', 'description', 'location',
            'open_time', 'close_time', 'owner',
            'trainers', 'image_file', 'image',
            'image', 'phone_number', 'price',
            'three_month_discount_price', 'six_month_discount_price',
            'twelve_month_discount_price', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'id']


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data)


    def get_image_url(self, obj):
        """Return full image URL"""
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return None





    def validate(self, data):
        """Cross-field validation"""
        # Check if open_time is before close_time
        open_time = data.get('open_time')
        close_time = data.get('close_time')

        if open_time and close_time and open_time >= close_time:
            raise serializers.ValidationError("Open time must be before close time")

        # Validate discount prices
        price = data.get('price')
        three_month_price = data.get('three_month_discount_price')
        six_month_price = data.get('six_month_discount_price')
        twelve_month_price = data.get('twelve_month_discount_price')

        if price:
            if three_month_price and three_month_price >= price:
                raise serializers.ValidationError("3-month discount price must be less than regular price")
            if six_month_price and six_month_price >= price:
                raise serializers.ValidationError("6-month discount price must be less than regular price")
            if twelve_month_price and twelve_month_price >= price:
                raise serializers.ValidationError("12-month discount price must be less than regular price")

        return data

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res





class GymListSerializer(serializers.ModelSerializer):
    """Simplified serializer for gym listing"""
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Gym
        fields = [
            'id', 'name', 'description', 'location', 'owner',
            'image', 'phone_number', 'price'
        ]



    def get_image_url(self, obj):
        if obj.image_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_file.url)
            return obj.image_file.url
        return None