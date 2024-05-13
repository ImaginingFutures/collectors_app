from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Bulk creates users from a list of emails provided via a file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the file containing email addresses, one per line')

    def handle(self, *args, **options):
        file_path = options['file_path']
        try:
            with open(file_path, 'r') as file:
                email_list = [line.strip() for line in file if line.strip()]
            for email in email_list:
                self.stdout.write(self.style.SUCCESS(f'Processing {email}'))
                try:
                    call_command('create_test_user', email)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to create user for {email}: {e}'))
                    import traceback
                    self.stdout.write(self.style.ERROR(traceback.format_exc()))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'The file {file_path} was not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
