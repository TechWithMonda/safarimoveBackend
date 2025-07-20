# management/commands/clean_expired_messages.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from chat.models import Message

class Command(BaseCommand):
    help = 'Deletes expired disappearing messages'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=24)
        expired = Message.objects.filter(
            is_disappearing=True,
            sent_at__lte=cutoff
        )
        count = expired.count()
        expired.delete()
        self.stdout.write(f'Deleted {count} expired messages')