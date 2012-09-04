import unittest

from tests.api.client import TestClient
from syncli.api.commands import CommandsApi


class CommandsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(CommandsApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def setUp(self):
        self.assertTrue(self.client.disco_hosts)

    def test_execute_command_success(self):
        """ Execute a command.
        """

        self.execute('ls -al', assertion=True)

    def test_execute_command_failure(self):
        """ Execute a command fails.
        """

        # Execute a non-existing command.
        self.execute('bioehfwefw -dkqjid', assertion=False)

    def execute(self, command, assertion=None):
        """
        """

        request = self.client.api.execute(command)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'executables')
                self.assertTrue(resp['resource_id'] == command)
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['cmd'] == command)
                self.assertTrue(resp['status']['returncode'] == 0)
                self.assertTrue(resp['status']['stdout'])
                self.assertFalse(resp['status']['stderr'])
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'executables')
                self.assertTrue(resp['resource_id'] == command)
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['cmd'] == command)
                self.assertTrue(resp['status']['returncode'] != 0)
                self.assertTrue(resp['status']['stderr'])
        else:
            return responses
