import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.cases.models import CaseFile, EvidenceItem
from apps.entities.models import Entity, Relationship
from apps.pipelines.models import PipelineSource
from apps.resources.models import Resource


class Command(BaseCommand):
    help = "Seed demo data for DarkMoney Lens"

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin_user, _ = user_model.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com"},
        )
        if not admin_user.has_usable_password():
            admin_user.set_password("admin1234")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()

        PipelineSource.objects.get_or_create(
            key="demo_resources",
            defaults={
                "name": "Demo Resource Directory",
                "description": "Static resource directory seed source.",
                "schedule_hint": "@daily",
            },
        )
        PipelineSource.objects.get_or_create(
            key="demo_finance",
            defaults={
                "name": "Demo Public Finance",
                "description": "Fixture-based finance source.",
                "schedule_hint": "@hourly",
            },
        )

        seed_path = Path(__file__).resolve().parents[4] / "fixtures" / "seed_data.json"
        data = json.loads(seed_path.read_text())

        case, _ = CaseFile.objects.get_or_create(
            title=data["cases"][0]["title"],
            defaults={
                "hypothesis": data["cases"][0]["hypothesis"],
                "status": data["cases"][0]["status"],
                "jurisdictions": data["cases"][0]["jurisdictions"],
                "targets": data["cases"][0]["targets"],
                "created_by": admin_user,
            },
        )

        entities = {}
        for entity in data["entities"]:
            record, _ = Entity.objects.get_or_create(
                canonical_name=entity["canonical_name"],
                defaults={
                    "type": entity["type"],
                    "aliases": entity["aliases"],
                    "identifiers": entity["identifiers"],
                    "jurisdiction": entity["jurisdiction"],
                },
            )
            entities[record.canonical_name] = record

        for relationship in data["relationships"]:
            from_entity = entities[relationship["from"]]
            to_entity = entities[relationship["to"]]
            Relationship.objects.get_or_create(
                from_entity=from_entity,
                to_entity=to_entity,
                rel_type=relationship["rel_type"],
                defaults={
                    "attributes": relationship.get("attributes", {}),
                    "provenance": relationship.get("provenance", {}),
                },
            )

        for evidence in data["evidence"]:
            resource = Resource.objects.filter(name=evidence["resource_name"]).first()
            EvidenceItem.objects.get_or_create(
                case=case,
                title=evidence["title"],
                defaults={
                    "claim_summary": evidence["claim_summary"],
                    "confidence": evidence["confidence"],
                    "occurred_at": evidence["occurred_at"],
                    "source_url": evidence["source_url"],
                    "notes": evidence["notes"],
                    "resource": resource,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed data loaded."))
