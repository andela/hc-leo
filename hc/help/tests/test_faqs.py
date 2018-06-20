from hc.test import BaseTestCase
from hc.help.models import Faq

class FaqTestCase(BaseTestCase):
    def setUp(self):
        self.faq = Faq.objects.create(question="what is", answer="foo bar")

    def test_it_works(self):
        r = self.client.get("/faq/")
        self.assertContains(r, "what is")
