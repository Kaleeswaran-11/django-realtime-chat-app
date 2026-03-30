from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from chat.models import Message, UserPresence


class Command(BaseCommand):
    help = 'Create sample users and chat messages for demo purposes.'

    def handle(self, *args, **options):
        demo_users = [
            ('alice', 'alice12345'),
            ('bob', 'bob12345'),
            ('charlie', 'charlie12345'),
        ]

        created = []
        for username, password in demo_users:
            user, was_created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com'})
            if was_created:
                user.set_password(password)
                user.save()
                created.append(username)
            UserPresence.objects.get_or_create(user=user)

        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        Message.objects.get_or_create(sender=alice, receiver=bob, content='Hello Bob! This is a seeded message.')
        Message.objects.get_or_create(sender=bob, receiver=alice, content='Hi Alice! Great to test this real-time chat app.')

        self.stdout.write(self.style.SUCCESS(f'Seed complete. Users ready: {", ".join(created) if created else "already existed"}'))
