from django.core.management.base import BaseCommand

from apps.pipelines.engine import bronze_to_silver, create_run


class Command(BaseCommand):
    help = "Rebuild silver layer from bronze"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True)

    def handle(self, *args, **options):
        run = create_run(options["source"])
        count = bronze_to_silver(run)
        self.stdout.write(self.style.SUCCESS(f"Rebuilt silver records: {count}"))
