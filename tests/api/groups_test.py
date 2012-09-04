import unittest
import uuid

from tests.api.client import TestClient
from syncli.api.groups import GroupsApi


class GroupsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(GroupsApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def setUp(self):
        self.assertTrue(self.client.disco_hosts)

    def test_create_success(self):
        """ Create a group.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=True)
        self.remove('unittest', assertion=None)

    def test_create_failure(self):
        """ Group creation fails when the group already
        exists.
        """

        self.create('root', assertion=False)

    def test_update_success(self):
        """ Group update works.
        """

        self.remove('unittest', assertion=None)
        self.remove('unittest2', assertion=None)
        self.create('unittest', assertion=None)
        self.update('unittest', 'unittest2', assertion=True)
        self.remove('unittest2', assertion=None)

    def test_update_failure(self):
        """ Group update fails.
        """

        self.remove('unittest', assertion=None)
        self.create('unittest', assertion=None)
        self.update('unittest', 'root', assertion=False)
        self.remove('unittest', assertion=None)

    def test_remove_success(self):
        """ Group deletion works.
        """

        self.create('unittest', assertion=None)
        self.remove('unittest', assertion=True)

    def test_remove_failure(self):
        """ Group deletion fails when the group does not exists.
        """

        # Generate a uuid group name to be sure that the group name
        # does not exist.
        group_name = '%s' % uuid.uuid4()
        self.remove(group_name, assertion=False)

    def update(self, group_name, new_name, assertion=None):
        request = self.client.api.update(group_name, new_name)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status'].get('name') == 'unittest2')
                self.assertTrue(resp['resource_id'] == 'unittest')
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == 'unittest')
                self.assertTrue('error' in resp)
        else:
            return responses

    def create(self, group_name, assertion=None):
        request = self.client.api.create(group_name)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue('gid' in resp['status'])
                self.assertTrue('members' in resp['status'])
                self.assertTrue('name' in resp['status'])
                self.assertTrue(resp['status']['name'] == 'unittest')
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == 'root')
                self.assertTrue('error' in resp)
        else:
            return responses

    def remove(self, group_name, assertion=None):
        request = self.client.api.remove(group_name)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == 'unittest')
                self.assertFalse('error' in resp)
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'groups')
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == group_name)
                self.assertTrue('error' in resp)
        else:
            return responses

if __name__ == '__main__':
    unittest.main()
