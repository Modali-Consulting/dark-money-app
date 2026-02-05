from rest_framework import serializers

from .models import Resource, ResourceCategory


class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    category_detail = ResourceCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Resource
        fields = "__all__"
