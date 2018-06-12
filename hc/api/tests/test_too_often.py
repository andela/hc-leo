from django.core import mail
from hc.test import BaseTestCase
from hc.api.models import Check


class TooOftenTestCase(BaseTestCase):

    def setUp(self):
        super(TooOftenTestCase, self).setUp()
        self.check = Check()
        self.check.user = self.alice
        self.check.name = "Test Check"
        self.check.save()

    def test_check_status_changes_to_often(self):
        # ping the check for the first time
        self.client.get("/ping/%s/" % self.check.code)
        # ping the check for the second time
        self.client.get("/ping/%s/" % self.check.code)
        self.check.refresh_from_db()
        self.assertEqual("often", self.check.status)
        # make sure an email is sent
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertEqual(msg.subject, "Test Check is running too often")


