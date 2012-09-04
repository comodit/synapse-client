import unittest

from tests.api.client import TestClient
from syncli.api.services import ServicesApi


class ServicesApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(ServicesApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def test_status_success(self):
        """Check if we can retrieve the status of an existing service"""
        name = "rsyslog"
        self.stop(name, assertion=None)
        self.status(name, assertion=True)

    def test_status_failure(self):
        """Check if retrieving status of non existing service returns an 
        error."""
        name = "qenqzeofnpndj"
        self.stop(name, assertion=None)
        self.status(name, assertion=False)

    def test_start_success(self):
        """Try starting an existing service"""
        name = "rsyslog"
        self.stop(name, assertion=None)
        self.start(name, assertion=True)

    def test_start_failure(self):
        """Try starting an unknown service"""
        name = "qenqzeofnpndj"
        self.start(name, assertion=False)

    def test_stop_success(self):
        """Try stopping an unknown service"""
        name = "rsyslog"
        self.start(name, assertion=None)
        self.stop(name, assertion=True)

    def test_stop_failure(self):
        """Try stopping an unknown service"""
        name = "qenqzeofnpndj"
        self.stop(name, assertion=False)

    def status(self, name, assertion=None):
        request = self.client.api.status(name)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
            if assertion is False:
                self.assertTrue(resp['status']['running'] is False)
                self.assertTrue(resp['status']['enabled'] is False)

    def start(self, name, assertion=None):
        request = self.client.api.start(name)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
                self.assertTrue(resp['status']['running'] is True)
            if assertion is False:
                self.assertFalse('error' not in resp)
                #self.assertFalse(resp['status']['running'] is True)

    def stop(self, name, assertion=None):
        request = self.client.api.stop(name)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
                self.assertTrue(resp['status']['running'] is False)
            if assertion is False:
                #self.assertFalse('error' not in resp)
                self.assertTrue(resp['status']['running'] is False)


if __name__ == '__main__':
    unittest.main()
