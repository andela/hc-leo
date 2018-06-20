import logging
import time

from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone
from hc.api.models import Check
from hc.accounts.models import Member
from hc.lib import emails

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends UP/DOWN email alerts'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """
        query = Check.objects.filter(user__isnull=False).select_related("user")

        now = timezone.now()
        going_down_from_up = query.filter(alert_after__lt=now, status="up")
        going_down_from_often = query.filter(alert_after__lt=now, status="often")
        going_up = query.filter(alert_after__gt=now, status="down")
        # Don't combine this in one query so Postgres can query using index:
        checks = list(going_down_from_up.iterator()) + list(going_up.iterator()) + \
            list(going_down_from_often.iterator())
        if not checks:
            return False

        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        check.save()

        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))
        errors = check.send_alert()
        self.send_team_notification(check)
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" % (ch.kind, ch.value, error))

        connection.close()
        return True

    def send_team_notification(self, check):
        """Send notification to members in a team depending on their priority"""

        team = Member.objects.filter(team=check.user.profile).order_by("priority")
        for member in team:
            if member.priority == "high" and not member.is_alerted(check):
                self.notify(check, member.user.email)
            elif member.priority == "low" and not member.is_alerted(check):
                self.notify(check, member.user.email)
        return True

    def notify(self, check, email):
        """helper function for notifying a user"""

        q = Check.objects.filter(user=check.user)
        ctx = {"checks": list(q), "check": check}
        emails.alert(email, ctx)
        check.alert_sent = True
        check.prev_alert_status = check.status
        check.save()

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)
