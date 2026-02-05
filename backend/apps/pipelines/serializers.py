from rest_framework import serializers

from .models import PipelineSource, PipelineRun, ServingProjection


class PipelineSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PipelineSource
        fields = "__all__"


class PipelineRunSerializer(serializers.ModelSerializer):
    source_detail = PipelineSourceSerializer(source="source", read_only=True)

    class Meta:
        model = PipelineRun
        fields = "__all__"


class ServingProjectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServingProjection
        fields = "__all__"
