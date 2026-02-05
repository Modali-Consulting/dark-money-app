from django.core.management.base import BaseCommand

from apps.pipelines.engine import create_run, publish_serving


class Command(BaseCommand):
    help = "Publish serving projections"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True)

    def handle(self, *args, **options):
        run = create_run(options["source"])
        projection = publish_serving(run)
        self.stdout.write(self.style.SUCCESS(f"Published serving projection: {projection.name}"))
