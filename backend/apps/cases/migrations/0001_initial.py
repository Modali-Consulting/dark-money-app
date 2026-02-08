from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CaseFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("hypothesis", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("open", "Open"), ("monitoring", "Monitoring"), ("closed", "Closed")], default="open", max_length=50)),
                ("jurisdictions", models.JSONField(blank=True, default=list)),
                ("targets", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EvidenceItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("claim_summary", models.TextField(blank=True)),
                ("confidence", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="medium", max_length=20)),
                ("occurred_at", models.DateField(blank=True, null=True)),
                ("source_url", models.URLField(blank=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "case",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="evidence", to="cases.casefile"),
                ),
                (
                    "resource",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="resources.resource"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CaseResource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("note", models.TextField(blank=True)),
                (
                    "case",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="saved_resources", to="cases.casefile"),
                ),
                (
                    "resource",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="resources.resource"),
                ),
            ],
            options={"unique_together": {("case", "resource")}},
        ),
        migrations.CreateModel(
            name="AttachmentMeta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("filename", models.CharField(max_length=255)),
                ("content_type", models.CharField(max_length=100)),
                ("sha256", models.CharField(max_length=64)),
                ("storage_ref", models.CharField(max_length=255)),
                (
                    "evidence",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="cases.evidenceitem"),
                ),
            ],
        ),
    ]
