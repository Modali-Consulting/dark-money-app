from django.db import models

from apps.cases.models import CaseFile


class Entity(models.Model):
    TYPE_CHOICES = [
        ("person", "Person"),
        ("org", "Organization"),
        ("committee", "Committee"),
        ("gov", "Government Body"),
        ("asset", "Asset"),
    ]

    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    canonical_name = models.CharField(max_length=255)
    aliases = models.JSONField(default=list, blank=True)
    identifiers = models.JSONField(default=dict, blank=True)
    jurisdiction = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.canonical_name


class Relationship(models.Model):
    from_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="outgoing_relationships")
    to_entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="incoming_relationships")
    rel_type = models.CharField(max_length=100)
    attributes = models.JSONField(default=dict, blank=True)
    provenance = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CaseEntity(models.Model):
    case = models.ForeignKey(CaseFile, on_delete=models.CASCADE, related_name="case_entities")
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    label = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("case", "entity")


class ChecklistItem(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name="checklist")
    case = models.ForeignKey(CaseFile, on_delete=models.SET_NULL, null=True, blank=True)
    step_key = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default="pending")
    note = models.TextField(blank=True)
    url = models.URLField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
