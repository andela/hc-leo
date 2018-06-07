from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone


class UnresolvedTestCase(BaseTestCase):

    def setUp(self):
        super(UnresolvedTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Failed check")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/unresolved/")
            self.assertEqual(r.status_code, 200)

    def test_it_contains_failed_check(self):
        self.check.last_ping = timezone.now() - td(days=3)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/unresolved/")

        self.assertContains(r, "Failed check")
