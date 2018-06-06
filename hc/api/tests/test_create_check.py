import json

from hc.api.models import Channel, Check
from hc.test import BaseTestCase


class CreateCheckTestCase(BaseTestCase):
    URL = "/api/v1/checks/"

    def setUp(self):
        super(CreateCheckTestCase, self).setUp()

    def post(self, data, expected_error=None):
        r = self.client.post(self.URL, json.dumps(data),
                             content_type="application/json")

        if expected_error:
            self.assertEqual(r.status_code, 400)
            ### Assert that the expected error is the response error
            self.assertEqual(expected_error, r.json()['error'])

        return r

    def test_it_works(self):
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "tags": "bar,baz",
            "timeout": 3600,
            "grace": 60
        })

        self.assertEqual(r.status_code, 201)

        doc = r.json()
        assert "ping_url" in doc
        self.assertEqual(doc["name"], "Foo")
        self.assertEqual(doc["tags"], "bar,baz")

        ### Assert the expected last_ping and n_pings values
        self.assertIsNone(doc["last_ping"])
        self.assertEquals(doc["n_pings"], 0)

        self.assertEqual(Check.objects.count(), 1)
        check = Check.objects.get()
        self.assertEqual(check.name, "Foo")
        self.assertEqual(check.tags, "bar,baz")
        self.assertEqual(check.timeout.total_seconds(), 3600)
        self.assertEqual(check.grace.total_seconds(), 60)

    def test_it_accepts_api_key_in_header(self):
        payload = json.dumps({"name": "Foo"})

        ### Make the post request and get the response
        r = self.client.post(self.URL,
                             payload,
                             content_type='application/json',
                             HTTP_X_API_KEY='abc')

        self.assertEqual(r.status_code, 201)


    def test_it_handles_missing_request_body(self):
        ### Make the post request with a missing body and get the response
        payload = json.dumps({"name": "Foo"})
        r = self.client.post(self.URL,
                             payload,
                             content_type='application/json',
                             HTTP_X_API_KEY='wrong_api_key')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["error"], "wrong api_key")

    def test_it_handles_invalid_json(self):
        ### Make the post request with invalid json data type
        r = self.client.post(self.URL,
                             {"payload"},
                             content_type='application/json',
                             HTTP_X_API_KEY='abc')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["error"], "could not parse request body")

    def test_it_rejects_wrong_api_key(self):
        r = self.post({"api_key": "wrong"},
                      expected_error="wrong api_key")

    def test_it_rejects_non_number_timeout(self):
        self.post({"api_key": "abc", "timeout": "oops"},
                  expected_error="timeout is not a number")

    def test_it_rejects_non_string_name(self):
        self.post({"api_key": "abc", "name": False},
                  expected_error="name is not a string")

    ### Test for the assignment of channels
    def test_assignment_of_channel(self):
        ch = Channel(user=self.alice, kind="pushbullet", value="test-token")
        ch.save()

        self.post({"api_key": "abc", "channels": "*"})

        check = Check.objects.get()
        self.assertEqual(check.channel_set.get(), ch)

    ### Test for the 'timeout is too small' and 'timeout is too large' errors
    def test_timeout_errors(self):
        # timeout is too large
        r = self.post({
            "api_key": "abc",
            "name": "Foo",
            "timeout": 3600000
        })

        self.assertEqual(r.json()["error"], "timeout is too large")

        # timeout is too small
        res = self.post({
            "api_key": "abc",
            "name": "Bar",
            "timeout": 0
        })

        self.assertEqual(res.json()["error"], "timeout is too small")
