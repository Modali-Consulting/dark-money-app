from django.db import models


class ResourceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Resource(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name="resources")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    jurisdiction = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    freshness_notes = models.TextField(blank=True)
    how_to_use = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
