from rest_framework import serializers

from .models import CaseFile, CaseResource, EvidenceItem, AttachmentMeta
from apps.resources.serializers import ResourceSerializer


class AttachmentMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentMeta
        fields = "__all__"


class EvidenceItemSerializer(serializers.ModelSerializer):
    attachments = AttachmentMetaSerializer(many=True, read_only=True)

    class Meta:
        model = EvidenceItem
        fields = "__all__"


class CaseResourceSerializer(serializers.ModelSerializer):
    resource_detail = ResourceSerializer(source="resource", read_only=True)

    class Meta:
        model = CaseResource
        fields = "__all__"


class CaseFileSerializer(serializers.ModelSerializer):
    evidence = EvidenceItemSerializer(many=True, read_only=True)
    saved_resources = CaseResourceSerializer(many=True, read_only=True)

    class Meta:
        model = CaseFile
        fields = "__all__"
