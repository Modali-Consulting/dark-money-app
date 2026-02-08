from django.core.management.base import BaseCommand

from apps.pipelines.engine import silver_to_gold, create_run


class Command(BaseCommand):
    help = "Build gold layer from silver"

    def add_arguments(self, parser):
        parser.add_argument("--source", required=True)

    def handle(self, *args, **options):
        run = create_run(options["source"])
        count = silver_to_gold(run)
        self.stdout.write(self.style.SUCCESS(f"Built gold entities/relationships: {count}"))
