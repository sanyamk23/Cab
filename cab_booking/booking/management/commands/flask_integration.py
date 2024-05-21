from django.core.management.base import BaseCommand
from subprocess import Popen

class Command(BaseCommand):
    help = 'Run the Flask app within Django'

    def handle(self, *args, **options):
        self.stdout.write('Starting Flask app...')

        # Use Popen to start the Flask app in a subprocess
        Popen(['flask', 'run'])

        self.stdout.write(self.style.SUCCESS('Flask app started successfully'))
