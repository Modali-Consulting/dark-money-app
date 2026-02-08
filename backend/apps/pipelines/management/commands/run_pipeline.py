from django.core.management.base import BaseCommand

from apps.pipelines.engine import run_pipeline


class Command(BaseCommand):
    help = "Run full medallion pipeline for a source"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True)

    def handle(self, *args, **options):
        source_key = options["source"]
        run = run_pipeline(source_key)
        self.stdout.write(self.style.SUCCESS(f"Pipeline run completed: {run.run_id}"))
