from django.conf import settings
from django.db import models

from apps.resources.models import Resource


class CaseFile(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("monitoring", "Monitoring"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=255)
    hypothesis = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open")
    jurisdictions = models.JSONField(default=list, blank=True)
    targets = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CaseResource(models.Model):
    case = models.ForeignKey(CaseFile, on_delete=models.CASCADE, related_name="saved_resources")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ("case", "resource")


class EvidenceItem(models.Model):
    CONFIDENCE_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    case = models.ForeignKey(CaseFile, on_delete=models.CASCADE, related_name="evidence")
    title = models.CharField(max_length=255)
    claim_summary = models.TextField(blank=True)
    confidence = models.CharField(max_length=20, choices=CONFIDENCE_CHOICES, default="medium")
    occurred_at = models.DateField(null=True, blank=True)
    source_url = models.URLField(blank=True)
    resource = models.ForeignKey(Resource, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class AttachmentMeta(models.Model):
    evidence = models.ForeignKey(EvidenceItem, on_delete=models.CASCADE, related_name="attachments")
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    sha256 = models.CharField(max_length=64)
    storage_ref = models.CharField(max_length=255)
