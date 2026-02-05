from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Entity, Relationship
from .serializers import EntitySerializer, RelationshipSerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all().order_by("canonical_name")
    serializer_class = EntitySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["canonical_name", "aliases", "identifiers"]


class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.select_related("from_entity", "to_entity").all()
    serializer_class = RelationshipSerializer
    permission_classes = [IsAuthenticated]


class GraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        nodes = EntitySerializer(Entity.objects.all(), many=True).data
        edges = RelationshipSerializer(Relationship.objects.all(), many=True).data
        return Response({"nodes": nodes, "edges": edges})

    def post(self, request):
        payload = request.data
        nodes = payload.get("nodes", [])
        edges = payload.get("edges", [])

        created_nodes = []
        for node in nodes:
            serializer = EntitySerializer(data=node)
            serializer.is_valid(raise_exception=True)
            created_nodes.append(serializer.save())

        created_edges = []
        for edge in edges:
            serializer = RelationshipSerializer(data=edge)
            serializer.is_valid(raise_exception=True)
            created_edges.append(serializer.save())

        return Response({"nodes": EntitySerializer(created_nodes, many=True).data,
                         "edges": RelationshipSerializer(created_edges, many=True).data},
                        status=status.HTTP_201_CREATED)
