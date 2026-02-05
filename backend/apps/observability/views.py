from django.http import HttpResponse
from django.utils import timezone

from apps.pipelines.models import BronzeRecord, GoldEntityMap, PipelineRun, SilverRecord


def metrics_view(request):
    total_bronze = BronzeRecord.objects.count()
    total_silver = SilverRecord.objects.count()
    total_gold = GoldEntityMap.objects.count()
    last_run = PipelineRun.objects.order_by("-started_at").first()
    last_run_age = 0
    if last_run:
        last_run_age = int((timezone.now() - last_run.started_at).total_seconds())

    output = [
        f"darkmoney_bronze_records {total_bronze}",
        f"darkmoney_silver_records {total_silver}",
        f"darkmoney_gold_records {total_gold}",
        f"darkmoney_last_run_age_seconds {last_run_age}",
    ]
    return HttpResponse("\n".join(output), content_type="text/plain")
