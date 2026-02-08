import uuid
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PipelineSource",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("enabled", models.BooleanField(default=True)),
                ("schedule_hint", models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="PipelineRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("run_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("running", "Running"), ("success", "Success"), ("failed", "Failed")], default="running", max_length=20)),
                ("stats", models.JSONField(blank=True, default=dict)),
                ("error", models.TextField(blank=True)),
                (
                    "source",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="pipelines.pipelinesource"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BronzeRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_key", models.CharField(max_length=100)),
                ("fetched_at", models.DateTimeField()),
                ("checksum", models.CharField(max_length=64)),
                ("payload_type", models.CharField(max_length=50)),
                ("payload_text", models.TextField(blank=True)),
                ("payload_bytes", models.BinaryField(blank=True, null=True)),
                ("request_params", models.JSONField(blank=True, default=dict)),
                ("pipeline_version", models.CharField(max_length=50)),
                ("uri", models.URLField(blank=True)),
                ("headers", models.JSONField(blank=True, default=dict)),
                (
                    "run",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="bronze_records", to="pipelines.pipelinerun"),
                ),
            ],
            options={"ordering": ["-fetched_at"]},
        ),
        migrations.CreateModel(
            name="SilverRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_key", models.CharField(max_length=100)),
                ("record_type", models.CharField(max_length=100)),
                ("normalized", models.JSONField(default=dict)),
                ("natural_key", models.CharField(max_length=255)),
                ("checksum", models.CharField(max_length=64)),
                ("observed_at", models.DateTimeField()),
                (
                    "run",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="silver_records", to="pipelines.pipelinerun"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GoldEntityMap",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("entity_id", models.CharField(max_length=100)),
                ("match_confidence", models.FloatField(default=0.0)),
                ("match_reason", models.TextField(blank=True)),
                (
                    "silver",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="pipelines.silverrecord"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ServingProjection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("version", models.CharField(max_length=50)),
                ("built_at", models.DateTimeField(auto_now_add=True)),
                ("stats", models.JSONField(blank=True, default=dict)),
            ],
        ),
    ]
