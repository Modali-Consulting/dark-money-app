import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from django.db import transaction

from .models import BronzeRecord, GoldEntityMap, PipelineRun, PipelineSource, SilverRecord, ServingProjection
from apps.entities.models import Entity, Relationship
from apps.resources.models import Resource, ResourceCategory

LOGGER = logging.getLogger(__name__)
PIPELINE_VERSION = "1.0"

FIXTURE_DIR = Path(__file__).resolve().parent.parent.parent / "fixtures"


def _checksum(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def create_run(source_key: str) -> PipelineRun:
    source = PipelineSource.objects.get(key=source_key)
    return PipelineRun.objects.create(source=source)


def write_bronze(run: PipelineRun, payload: bytes, metadata: dict) -> BronzeRecord:
    return BronzeRecord.objects.create(
        run=run,
        source_key=run.source.key,
        fetched_at=metadata.get("fetched_at", datetime.now(timezone.utc)),
        checksum=_checksum(payload),
        payload_type=metadata.get("payload_type", "json"),
        payload_text=payload.decode("utf-8"),
        request_params=metadata.get("request_params", {}),
        pipeline_version=PIPELINE_VERSION,
        uri=metadata.get("uri", ""),
        headers=metadata.get("headers", {}),
    )


def extract_demo_resources(run: PipelineRun) -> BronzeRecord:
    payload_path = FIXTURE_DIR / "demo_resources.json"
    payload = payload_path.read_bytes()
    metadata = {
        "payload_type": "json",
        "request_params": {"fixture": "demo_resources.json"},
        "uri": "file://fixtures/demo_resources.json",
    }
    LOGGER.info("extract_demo_resources_start")
    record = write_bronze(run, payload, metadata)
    LOGGER.info("extract_demo_resources_end")
    return record


def extract_demo_finance(run: PipelineRun) -> BronzeRecord:
    payload_path = FIXTURE_DIR / "demo_finance.json"
    payload = payload_path.read_bytes()
    metadata = {
        "payload_type": "json",
        "request_params": {"fixture": "demo_finance.json"},
        "uri": "file://fixtures/demo_finance.json",
    }
    LOGGER.info("extract_demo_finance_start")
    record = write_bronze(run, payload, metadata)
    LOGGER.info("extract_demo_finance_end")
    return record


def bronze_to_silver(run: PipelineRun) -> int:
    count = 0
    for bronze in run.bronze_records.all():
        payload = json.loads(bronze.payload_text)
        if bronze.source_key == "demo_resources":
            for category in payload.get("categories", []):
                SilverRecord.objects.create(
                    run=run,
                    source_key=bronze.source_key,
                    record_type="resource_category",
                    normalized=category,
                    natural_key=category["name"],
                    checksum=_checksum(json.dumps(category).encode("utf-8")),
                    observed_at=bronze.fetched_at,
                )
                count += 1
            for resource in payload.get("resources", []):
                SilverRecord.objects.create(
                    run=run,
                    source_key=bronze.source_key,
                    record_type="resource",
                    normalized=resource,
                    natural_key=resource["name"],
                    checksum=_checksum(json.dumps(resource).encode("utf-8")),
                    observed_at=bronze.fetched_at,
                )
                count += 1
        if bronze.source_key == "demo_finance":
            for record in payload.get("records", []):
                SilverRecord.objects.create(
                    run=run,
                    source_key=bronze.source_key,
                    record_type=record["record_type"],
                    normalized=record,
                    natural_key=record["natural_key"],
                    checksum=_checksum(json.dumps(record).encode("utf-8")),
                    observed_at=bronze.fetched_at,
                )
                count += 1
    return count


def silver_to_gold(run: PipelineRun) -> int:
    created = 0
    for silver in run.silver_records.all():
        if silver.record_type == "resource_category":
            ResourceCategory.objects.get_or_create(
                name=silver.normalized["name"],
                defaults={"description": silver.normalized.get("description", "")},
            )
        if silver.record_type == "resource":
            category, _ = ResourceCategory.objects.get_or_create(
                name=silver.normalized["category"],
                defaults={"description": ""},
            )
            Resource.objects.get_or_create(
                name=silver.normalized["name"],
                defaults={
                    "category": category,
                    "description": silver.normalized.get("description", ""),
                    "tags": silver.normalized.get("tags", []),
                    "jurisdiction": silver.normalized.get("jurisdiction", ""),
                    "type": silver.normalized.get("type", ""),
                    "url": silver.normalized.get("url", ""),
                    "freshness_notes": silver.normalized.get("freshness_notes", ""),
                    "how_to_use": silver.normalized.get("how_to_use", ""),
                },
            )
        if silver.record_type == "entity":
            entity, _ = Entity.objects.get_or_create(
                canonical_name=silver.normalized["canonical_name"],
                defaults={
                    "type": silver.normalized.get("type", "org"),
                    "aliases": silver.normalized.get("aliases", []),
                    "identifiers": silver.normalized.get("identifiers", {}),
                    "jurisdiction": silver.normalized.get("jurisdiction", ""),
                },
            )
            GoldEntityMap.objects.create(
                silver=silver,
                entity_id=str(entity.id),
                match_confidence=0.9,
                match_reason="Exact match on canonical_name",
            )
            created += 1
        if silver.record_type == "relationship":
            from_entity = Entity.objects.filter(canonical_name=silver.normalized["from"]).first()
            to_entity = Entity.objects.filter(canonical_name=silver.normalized["to"]).first()
            if from_entity and to_entity:
                Relationship.objects.get_or_create(
                    from_entity=from_entity,
                    to_entity=to_entity,
                    rel_type=silver.normalized["rel_type"],
                    defaults={
                        "attributes": silver.normalized.get("attributes", {}),
                        "provenance": silver.normalized.get("provenance", {}),
                    },
                )
                created += 1
    return created


def publish_serving(run: PipelineRun) -> ServingProjection:
    stats = {
        "entities": Entity.objects.count(),
        "relationships": Relationship.objects.count(),
        "resources": Resource.objects.count(),
    }
    return ServingProjection.objects.create(name="serving_entity_search", version=PIPELINE_VERSION, stats=stats)


def run_pipeline(source_key: str) -> PipelineRun:
    with transaction.atomic():
        run = create_run(source_key)
        if source_key == "demo_resources":
            extract_demo_resources(run)
        elif source_key == "demo_finance":
            extract_demo_finance(run)
        silver_count = bronze_to_silver(run)
        gold_count = silver_to_gold(run)
        publish_serving(run)
        run.status = "success"
        run.stats = {"silver_count": silver_count, "gold_count": gold_count}
        run.finished_at = datetime.now(timezone.utc)
        run.save()
    return run
