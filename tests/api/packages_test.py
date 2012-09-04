import unittest
import uuid

from tests.api.client import TestClient
from syncli.api.packages import PackagesApi


class PackagesApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.client = TestClient(PackagesApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def setUp(self):
        self.assertTrue(self.client.disco_hosts)

    def test_install_success(self):
        """ Install a package.
        """

        self.install('htop', assertion=True)
        self.uninstall('htop', assertion=None)

    def test_install_failure(self):
        """ Install a package fails.
        """

        package = "%s" % uuid.uuid4()
        self.install(package, assertion=False)

    def test_remove_success(self):
        """ Remove a package.
        """

        self.install('htop', assertion=None)
        self.uninstall('htop', assertion=True)

    def test_remove_failure(self):
        """ Remove a package fails.
        """

        package = "%s" % uuid.uuid4()
        self.uninstall(package, assertion=False)

    def test_update_success(self):
        """ Update a package.
        """

        self.install('htop', assertion=None)
        self.update('htop', assertion=True)

    def test_update_failure(self):
        """ Update a package fails.
        """

        package = "%s" % uuid.uuid4()
        self.update(package, assertion=False)

    #def test_update_whole_success(self):
    #    """ Update the whole system package.
    #    """

    #    self.update(assertion=True)

    def install(self, package, assertion=None):
        request = self.client.api.install(package)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['installed'] == True)
                self.assertTrue(resp['resource_id'] == package)
                self.assertTrue(resp['collection'] == 'packages')
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == package)
                self.assertTrue(resp['collection'] == 'packages')
                self.assertTrue('error' in resp)
        else:
            return responses

    def uninstall(self, package, assertion=None):
        request = self.client.api.remove(package)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['status'])
                self.assertTrue(resp['status']['installed'] == False)
                self.assertTrue(resp['resource_id'] == package)
                self.assertTrue(resp['collection'] == 'packages')
        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == package)
                self.assertTrue(resp['collection'] == 'packages')
        else:
            return responses

    def update(self, package=None, assertion=None):
        request = self.client.api.update(package)
        self.client.send(request)
        responses = self.client.get_responses()

        if assertion is True:
            for resp in responses:
                self.assertTrue(resp['collection'] == 'packages')
                if package:
                    self.assertTrue(resp['status'])
                    self.assertTrue(resp['status']['installed'] == True)
                    self.assertTrue(resp['resource_id'] == package)

        elif assertion is False:
            for resp in responses:
                self.assertTrue(resp['status'])
                self.assertTrue(resp['resource_id'] == package)
                self.assertTrue(resp['collection'] == 'packages')
                self.assertTrue('error' in resp)
        else:
            return responses

if __name__ == '__main__':
    unittest.main()
