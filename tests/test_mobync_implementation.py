import json

from mobync import Diff
from mobync import Mobync
from mobync import ReadFilter, FilterType

from examples.in_memory_server_example.implementation import Implementation
from examples.in_memory_server_example.mock_data_base import DataBase
from examples.in_memory_server_example.models import Model1, Diff as UserDefinedDiff
import unittest


class TestSyncProtocol(unittest.TestCase):
    """
    Tests the sync protocol behavior.
    """
    @classmethod
    def setUpClass(cls):
        cls.db = DataBase()
        cls.db.add_table('diffs', [], UserDefinedDiff)
        cls.db.add_table('model1', [], Model1)
        cls.implementation = Implementation(cls.db)
        cls.mobync = Mobync(cls.implementation)

        cls.owner_id = "owner_1"

    def test_diff_validation(self):
        # Test incomplete diff
        with self.assertRaises(Exception):
            self.mobync._Mobync__validate_diff({}, self.owner_id)

        # Test valid diff
        valid_create_diff = {
            "id": "1",
            "owner":  self.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123774,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"a\"}"
        }
        self.assertTrue(self.mobync._Mobync__validate_diff(valid_create_diff, self.owner_id))

        # Test unauthorized diff
        with self.assertRaises(Exception):
            self.mobync._Mobync__validate_diff(valid_create_diff, "owner_2")

    def test_apply_diff(self):
        create_diff = {
            "id": "1",
            "owner":  self.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123774,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"a\"}"
        }
        self.mobync._Mobync__apply_diff(create_diff)

        res = self.mobync.synchronizer.read('diffs', [ReadFilter(Diff.OWNER, FilterType.equal,  self.owner_id)])
        self.assertEqual(json.loads(res), [create_diff])

        update_diff = {
            "id": "2",
            "owner":  self.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123775,
            "type": "update",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"b\"}"
        }
        self.assertTrue(self.mobync._Mobync__validate_diff(update_diff, self.owner_id))
        self.mobync._Mobync__apply_diff(update_diff)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal,  self.owner_id)])
        self.assertEqual(json.loads(res), [create_diff, update_diff])

        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [{'field1': 'b', 'id': 'uuid1'}])

        delete_diff = {
            "id": "3",
            "owner":  self.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123776,
            "type": "delete",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\"}"
        }
        self.assertTrue(self.mobync._Mobync__validate_diff(delete_diff, self.owner_id))
        self.mobync._Mobync__apply_diff(delete_diff)
        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal,  self.owner_id)])
        self.assertEqual(json.loads(res), [create_diff, update_diff, delete_diff])
        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [])
