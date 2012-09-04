import unittest
import hashlib

from tests.api.client import TestClient
from syncli.api.files import FilesApi


class FilesApiTest(unittest.TestCase):

    content = "All your files are belong to us !"

    @classmethod
    def setUpClass(self):
        self.client = TestClient(FilesApi)

    @classmethod
    def tearDownClass(self):
        self.client.disconnect()

    def test_infos_success(self):
        """ Retrieve the status of a file.
        """

        filename = "/tmp/test"
        self.create(filename, self.content, assertion=None)
        self.read(filename, assertion=True)
        self.delete(filename, assertion=None)

    def test_infos_failure(self):
        """ Read on non-existing file produces an error.
        """

        filename = "/tmp/test"
        self.delete(filename, assertion=None)
        self.read(filename, assertion=False)

    def test_create_success(self):
        """ Create a file.
        """

        filename = "/tmp/test"
        self.create(filename, self.content, assertion=True)
        self.delete(filename, assertion=None)

    def test_update_meta_success(self):
        """ Update the metadata of a file.
        """

        filename = "/tmp/test"
        mode = '755'
        self.create(filename, self.content, mode=mode, assertion=True)
        self.delete(filename, assertion=None)

    def test_update_meta_failure(self):
        """ Set mode 999 on a file must fail.
        """

        filename = "/tmp/test"
        mode = '999'
        self.create(filename, self.content, mode=mode, assertion=True)
        self.delete(filename, assertion=None)

    def test_delete_success(self):
        """ Delete a file.
        """

        filename = "/tmp/test"
        self.create(filename, self.content, assertion=None)
        self.delete(filename, assertion=True)

    def test_delete_failure(self):
        """ Delete an non-existing file must fail.
        """

        filename = "/tmp/test"
        self.create(filename, self.content, assertion=None)
        self.delete(filename, assertion=None)
        self.delete(filename, assertion=False)

    def read(self, path, assertion=None):
        request = self.client.api.infos(path, md5=True, content=True)
        self.client.send(request)
        responses = self.client.get_responses()
        content_md5 = self.md5_str(self.content)

        for resp in responses:
            if assertion:
                self.assertTrue(resp['status']['present'] is True)
                self.assertTrue('md5' in resp['status'])
                remote_md5 = resp['status']['md5']
                self.assertTrue(remote_md5 == content_md5)
            if assertion is False:
                self.assertFalse('error' not in resp)

    def create(self, path, content, owner=None, group=None, mode=None,
               assertion=None):
        request = self.client.api.create(path, content)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
                self.assertTrue(resp['status']['present'] is True)

    def update_meta(self, path, owner=None, group=None, mode=None,
               assertion=None):
        request = self.client.api.update_meta(path, mode=mode)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
                self.assertTrue(resp['status']['mode'] == mode)
            if assertion is False:
                self.assertFalse('error' not in resp)

    def delete(self, path, assertion=None):
        request = self.client.api.delete(path)
        self.client.send(request)
        responses = self.client.get_responses()

        for resp in responses:
            if assertion:
                self.assertTrue('error' not in resp)
                self.assertTrue(resp['status']['present'] is False)
            if assertion is False:
                self.assertFalse('error' not in resp)

    def md5_str(self, content):
        m = hashlib.md5()
        m.update(content)
        return m.hexdigest()


if __name__ == '__main__':
    unittest.main()
