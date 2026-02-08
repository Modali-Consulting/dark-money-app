from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.resources import views as resource_views
from apps.cases import views as case_views
from apps.entities import views as entity_views
from apps.pipelines import views as pipeline_views
from apps.observability import views as observability_views

router = routers.DefaultRouter()
router.register(r"resources", resource_views.ResourceViewSet)
router.register(r"resource-categories", resource_views.ResourceCategoryViewSet)
router.register(r"cases", case_views.CaseFileViewSet)
router.register(r"evidence", case_views.EvidenceItemViewSet)
router.register(r"case-resources", case_views.CaseResourceViewSet)
router.register(r"entities", entity_views.EntityViewSet)
router.register(r"relationships", entity_views.RelationshipViewSet)
router.register(r"pipeline-sources", pipeline_views.PipelineSourceViewSet)
router.register(r"pipeline-runs", pipeline_views.PipelineRunViewSet)
router.register(r"serving-projections", pipeline_views.ServingProjectionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/graph/", entity_views.GraphView.as_view()),
    path("api/pipelines/run/<uuid:run_id>/lineage/", pipeline_views.PipelineLineageView.as_view()),
    path("api/metrics/", observability_views.metrics_view),
    path("api/cases/<int:pk>/export/", case_views.export_case_pdf),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
