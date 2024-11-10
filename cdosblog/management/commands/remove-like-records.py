import os
import tarfile

from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from cdosblog.models import Like


class Command(BaseCommand):
    # https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/
    help = "Deletes records of IPs that liked a post."

    def handle(self, *args, **options):
        count = 0
        today = datetime.now(tz=timezone.utc)
        cutoff = today - timedelta(days=1)
        qs = Like.objects.all()
        for l in qs:
            if l.datetime <= cutoff:
                count += 1
                l.delete()
        self.stdout.write(self.style.SUCCESS("Successfully deleted {} like records".format(count)))
