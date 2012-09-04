import unittest

from tests.api.client import TestClient
from syncli.api.hosts import HostsApi


class HostsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(HostsApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def test_status(self):
        request = self.client.api.infos()
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            self.assertTrue('error' not in resp)

    def test_status_attr(self):

        for attr in self.client.api._attrs:
            request = self.client.api.infos([attr])
            self.client.send(request)
            responses = self.client.get_responses()

            for resp in responses:
                self.assertTrue(attr in resp['status'])
                self.assertTrue('error' not in resp)

    def test_status_attrs(self):

        attrs = self.client.api._attrs
        request = self.client.api.infos(attrs)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            # Ensure that resp['attributes'] contains all
            # self.client.api._attrs attributes.
            difference = set(resp['status']) - set(attrs)
            self.assertFalse(len(difference))

            self.assertTrue('error' not in resp)

if __name__ == '__main__':
    unittest.main()
