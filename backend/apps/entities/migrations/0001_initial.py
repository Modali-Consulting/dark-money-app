from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cases", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Entity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("type", models.CharField(choices=[("person", "Person"), ("org", "Organization"), ("committee", "Committee"), ("gov", "Government Body"), ("asset", "Asset")], max_length=50)),
                ("canonical_name", models.CharField(max_length=255)),
                ("aliases", models.JSONField(blank=True, default=list)),
                ("identifiers", models.JSONField(blank=True, default=dict)),
                ("jurisdiction", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Relationship",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rel_type", models.CharField(max_length=100)),
                ("attributes", models.JSONField(blank=True, default=dict)),
                ("provenance", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "from_entity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="outgoing_relationships", to="entities.entity"),
                ),
                (
                    "to_entity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="incoming_relationships", to="entities.entity"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CaseEntity",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=100)),
                (
                    "case",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="case_entities", to="cases.casefile"),
                ),
                (
                    "entity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="entities.entity"),
                ),
            ],
            options={"unique_together": {("case", "entity")}},
        ),
        migrations.CreateModel(
            name="ChecklistItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("step_key", models.CharField(max_length=100)),
                ("label", models.CharField(max_length=255)),
                ("status", models.CharField(default="pending", max_length=50)),
                ("note", models.TextField(blank=True)),
                ("url", models.URLField(blank=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "case",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="cases.casefile"),
                ),
                (
                    "entity",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="checklist", to="entities.entity"),
                ),
            ],
        ),
    ]
