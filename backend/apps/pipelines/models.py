import uuid
from django.db import models


class PipelineSource(models.Model):
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)
    schedule_hint = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class PipelineRun(models.Model):
    STATUS_CHOICES = [
        ("running", "Running"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]

    run_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    source = models.ForeignKey(PipelineSource, on_delete=models.CASCADE, related_name="runs")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="running")
    stats = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True)


class BronzeRecord(models.Model):
    run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, related_name="bronze_records")
    source_key = models.CharField(max_length=100)
    fetched_at = models.DateTimeField()
    checksum = models.CharField(max_length=64)
    payload_type = models.CharField(max_length=50)
    payload_text = models.TextField(blank=True)
    payload_bytes = models.BinaryField(null=True, blank=True)
    request_params = models.JSONField(default=dict, blank=True)
    pipeline_version = models.CharField(max_length=50)
    uri = models.URLField(blank=True)
    headers = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-fetched_at"]


class SilverRecord(models.Model):
    run = models.ForeignKey(PipelineRun, on_delete=models.CASCADE, related_name="silver_records")
    source_key = models.CharField(max_length=100)
    record_type = models.CharField(max_length=100)
    normalized = models.JSONField(default=dict)
    natural_key = models.CharField(max_length=255)
    checksum = models.CharField(max_length=64)
    observed_at = models.DateTimeField()


class GoldEntityMap(models.Model):
    silver = models.ForeignKey(SilverRecord, on_delete=models.SET_NULL, null=True, blank=True)
    entity_id = models.CharField(max_length=100)
    match_confidence = models.FloatField(default=0.0)
    match_reason = models.TextField(blank=True)


class ServingProjection(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    built_at = models.DateTimeField(auto_now_add=True)
    stats = models.JSONField(default=dict, blank=True)
