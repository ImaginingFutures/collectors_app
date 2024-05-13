from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import csv

class Command(BaseCommand):
    help = 'Exports user IDs and emails to a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, help='Filename to write to', default='users.csv')

    def handle(self, *args, **options):
        filename = options['filename']
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'email'])  # Writing header

            for user in User.objects.all().values_list('id', 'email'):
                writer.writerow(user)  # Writing user data

            self.stdout.write(self.style.SUCCESS(f'Successfully exported all users to {filename}'))
