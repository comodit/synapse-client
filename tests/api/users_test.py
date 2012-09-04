import unittest
import uuid

from tests.api.client import TestClient
from syncli.api.users import UsersApi


class UserssApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(UsersApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def setUp(self):
        self.assertTrue(self.client.disco_hosts)

    def test_create_success(self):
        """ Create a user.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=True)
        self.remove('unittest', assertion=None)

    def test_create_failure(self):
        """ Create a user fails.
        """

        self.create('root', assertion=False)

    def test_create_password_success(self):
        """ Create a user with a password.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', 'secret', assertion=True)
        self.remove('unittest', assertion=None)

    def test_remove_success(self):
        """ Remove a user.
        """

        self.create('unittest', assertion=None)
        self.remove('unittest', assertion=True)

    def test_remove_failure(self):
        """ Remove a user fails.
        """

        username = '%s' % uuid.uuid4()
        self.remove(username, assertion=False)

    def test_add_group_success(self):
        """ Add a group (as list) to the user.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=None)

        responses = self.update('unittest', add_to_groups=['root'],
                                assertion=True)
        for resp in responses:
            self.assertTrue('root' in resp['status']['groups'])

        self.remove('unittest', assertion=None)

    def test_add_str_group_success(self):
        """ Add a group (as string) to the user.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=None)

        responses = self.update('unittest', add_to_groups='root',
                                assertion=True)
        for resp in responses:
            self.assertTrue('root' in resp['status']['groups'])

        self.remove('unittest', assertion=None)

    def test_add_group_failure(self):
        """ Add a group to the user fails.
        """

        group_name = "%s" % uuid.uuid4()

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=None)
        self.update('unittest', add_to_groups=group_name, assertion=False)
        self.remove('unittest', assertion=None)

    def create(self, username, password=None, assertion=None):
        request = self.client.api.create(username, password)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == username)
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['shell'])
                self.assertTrue(resp['status']['uid'])
                self.assertTrue(resp['status']['gid'])
                self.assertTrue(resp['status']['groups'])
                self.assertTrue(resp['status']['dir'])
                self.assertTrue(resp['status']['name'] == username)
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == username)
                self.assertTrue('error' in resp)
        else:
            return responses

    def remove(self, username, assertion=None):
        request = self.client.api.remove(username)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == username)
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == username)
                self.assertTrue('error' in resp)
        else:
            return responses

    def update(self, name, password=None, login_group=None, add_to_groups=None,
               remove_from_groups=None, set_groups=None, monitor=None,
               assertion=None):

        request = self.client.api.update(name, password, login_group,
                                         add_to_groups, remove_from_groups,
                                         set_groups, monitor)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == name)
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['groups'])
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'users')
                self.assertTrue(resp['resource_id'] == name)
                self.assertTrue('error' in resp)

        return responses


if __name__ == '__main__':
    unittest.main()
