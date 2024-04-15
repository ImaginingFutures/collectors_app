import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

class Command(BaseCommand):
    help = 'Create a test user without a password'
    
    def add_arguments(self, parser) -> None:
         parser.add_argument('email', type=str, help='Email address for the test user')

    def handle(self, *args, **options):
        email = options['email']
        
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, email):
            raise ValidationError(f"The email {email} is not a valid email address.")

        username = email  # Using email as username for simplicity

        password = get_random_string(length=10)
        user, created = User.objects.get_or_create(email=email, username=username)
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created test user: {email}'))
        else:
            self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
