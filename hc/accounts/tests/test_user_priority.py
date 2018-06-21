from django.core import mail
from django.contrib.auth.models import User
from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check
from hc.api.management.commands.sendalerts import Command


class UserPriorityTestCase(BaseTestCase):
    def setUp(self):
        super(UserPriorityTestCase, self).setUp()

        check = Check(name="Test Check")
        check.status = "down"
        check.user = self.alice
        check.save()

    def test_it_sets_user_priority(self):
        self.client.login(username="alice@example.org", password="password")
        form = {
            "invite_team_member": "1", "email": "frank@example.org", "check": "Test Check"}
        self.client.post("/accounts/profile/", form)

        form = {
            "set_notification_priority": "1",
            "priority": "high",
            "member_email": "frank@example.org"
        }
        self.client.post("/accounts/profile/", form)

        user = User.objects.filter(email=form["member_email"]).first()
        member = Member.objects.filter(user=user).first()
        self.assertEqual(member.priority, "high")

    def test_higher_priority_user_gets_notified_first(self):
        check = Check.objects.filter(name="Test Check").first()
        self.client.login(username="alice@example.org", password="password")

        # the user bob@example.org is already in alice's team (set up in BaseTestCase)
        # so we invite one more user and give them a high priority
        form = {
            "invite_team_member": "1", "email": "george@example.org", "check": "Test Check"}
        self.client.post("/accounts/profile/", form)

        form = {
            "set_notification_priority": "1",
            "priority": "high",
            "member_email": "george@example.org"
        }
        self.client.post("/accounts/profile/", form)

        Command().send_team_notification(check)
        # assert for two emails because one is an invitation email
        self.assertEqual(len(mail.outbox), 2)
        self.assertNotIn("bob@example.org", mail.outbox)










