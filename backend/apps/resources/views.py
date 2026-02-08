from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Resource, ResourceCategory
from .serializers import ResourceSerializer, ResourceCategorySerializer


class ResourceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ResourceCategory.objects.all().order_by("name")
    serializer_class = ResourceCategorySerializer
    permission_classes = [IsAuthenticated]


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.select_related("category").all().order_by("name")
    serializer_class = ResourceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category", "jurisdiction", "type"]
    search_fields = ["name", "description", "tags"]
