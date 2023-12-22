import json
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from aerospike_provider.hooks.aerospike import AerospikeHook, AirflowException

class TestAerospikeHookConn(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.connection = mock.MagicMock()
        self.connection.host = "localhost"
        self.connection.port = 3000

        class UnitTestAerospikeHook(AerospikeHook):
            conn_name_attr = "aerospike_conn_id"

        self.hook = UnitTestAerospikeHook()
        self.hook.get_conn = mock.Mock()
        self.hook.get_connection = mock.Mock()
        self.hook.get_connection.return_value = self.connection
        # self.hook.get_connection = mock.Mock()
        # self.hook.get_connection.return_value = self.connection
        # self.hook.client = mock.Mock()
        # self.hook.get_conn.return_value = self.connection

    # fix this test
    # @patch('aerospike.client')
    # def test_get_conn_new_connection(self, mock_client):
    #     # mock_get_connection.return_value = MagicMock(host='localhost', port=3000)
        
    #     mock_client_instance = MagicMock(host='localhost', port=3000)
    #     mock_client.connect.return_value = mock_client_instance # patch aerospike.client
    #     mock_client_instance.connect.return_value = mock_client_instance # mock aerospike.client

    #     # connection = self.hook.get_connection()
    #     mock_client = mock_client.connect
    #     # print(f"connection ~~~~ {connection}")
    #     # print(f"client_instance ~~~ {client_instance}")
    #     print(f"mock_client_instance ~~~ {mock_client_instance}")
    #     print(f"mock_client ~~~ {mock_client}")
    #     print("Mock client calls:", mock_client.mock_details)  # Debugging output
    #     mock_client_instance
    #     # Verify that aerospike.client was called with the expected config
    #     mock_client_instance.assert_called_with(mock_client_instance)

    #     # Verify that a client instance was returned
    #     self.assertIsNotNone(mock_client_instance)

    def test_get_connection(self):
        connection = self.hook.get_connection()
        assert self.connection.port == connection.port
        assert self.connection.host == connection.host




class TestAerospikeHook(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.connection = mock.MagicMock()
        self.connection.host = "localhost"
        self.connection.port = 3000

        class UnitTestAerospikeHook(AerospikeHook):
            conn_name_attr = "aerospike_conn_id"

        self.hook = UnitTestAerospikeHook()
        self.hook.get_conn = mock.Mock()
        self.hook.get_connection = mock.Mock()
        self.hook.get_connection.return_value = self.connection


    def test_get_ui_field_behaviour(self):
        expected = {
            "hidden_fields": ["schema", "login", "password"],
            "relabeling": {
                "host": "host",
                "port": "port"
            },
            "placeholders": {
                "port": "3000",
                "host": "cluster node address (The client will learn about the other nodes in the cluster from the seed node)"
            },
        }
        assert self.hook.get_ui_field_behaviour() == expected


class TestAerospikeHookExistsMethod(unittest.TestCase):

    def setUp(self):
        self.hook = AerospikeHook()
        self.hook.client = MagicMock()

    def test_exists_single_key(self):
        test_namespace = 'test_namespace'
        test_set = 'test_set'
        test_key = 'test_key'
        test_policy = {}

        # Mock the client's exists method
        self.hook.client.exists.return_value = (True, {})

        result = self.hook.exists(test_namespace, test_set, test_key, test_policy)

        # Check if the client's exists method was called with the correct arguments
        self.hook.client.exists.assert_called_with((test_namespace, test_set, test_key), test_policy)

        # Check the result type
        self.assertIsInstance(result, tuple)

    def test_exists_multiple_keys(self):
        test_namespace = 'test_namespace'
        test_set = 'test_set'
        test_keys = ['key1', 'key2']
        test_policy = {}

        # Mock the client's exists_many method
        self.hook.client.exists_many.return_value = [True, False]

        result = self.hook.exists(test_namespace, test_set, test_keys, test_policy)

        # Check if the client's exists_many method was called with the correct arguments
        expected_keys = [(test_namespace, test_set, k) for k in test_keys]
        self.hook.client.exists_many.assert_called_with(expected_keys, test_policy)

        # Check the result type
        self.assertIsInstance(result, list)

    def test_exists_with_uninitialized_client(self):
        self.hook.client = None
        
        with self.assertRaises(AirflowException):
            self.hook.exists('namespace', 'set', 'key', {})


