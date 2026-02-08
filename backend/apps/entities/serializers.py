from rest_framework import serializers

from .models import Entity, Relationship, CaseEntity, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    checklist = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Entity
        fields = "__all__"


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"


class CaseEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseEntity
        fields = "__all__"
