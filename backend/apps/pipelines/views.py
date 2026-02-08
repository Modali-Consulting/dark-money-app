from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PipelineSource, PipelineRun, BronzeRecord, SilverRecord, GoldEntityMap, ServingProjection
from .serializers import PipelineSourceSerializer, PipelineRunSerializer, ServingProjectionSerializer


class PipelineSourceViewSet(viewsets.ModelViewSet):
    queryset = PipelineSource.objects.all().order_by("name")
    serializer_class = PipelineSourceSerializer
    permission_classes = [IsAuthenticated]


class PipelineRunViewSet(viewsets.ModelViewSet):
    queryset = PipelineRun.objects.select_related("source").all().order_by("-started_at")
    serializer_class = PipelineRunSerializer
    permission_classes = [IsAuthenticated]


class ServingProjectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServingProjection.objects.all().order_by("-built_at")
    serializer_class = ServingProjectionSerializer
    permission_classes = [IsAuthenticated]


class PipelineLineageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, run_id):
        run = PipelineRun.objects.get(run_id=run_id)
        bronze = BronzeRecord.objects.filter(run=run).count()
        silver = SilverRecord.objects.filter(run=run).count()
        gold = GoldEntityMap.objects.filter(silver__run=run).count()
        return Response({"run_id": str(run.run_id), "bronze": bronze, "silver": silver, "gold": gold})
