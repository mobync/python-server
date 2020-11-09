import json
from pprint import pprint

from mobync import OperationType, Diff
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

        cls.create_diff = {
            "id": "1",
            "owner": "owner_id",
            "logical_clock": 0,
            "utc_timestamp": 1604114123774,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"a\"}"
        }
        cls.update_diff = {
            "id": "2",
            "owner": "owner_id",
            "logical_clock": 0,
            "utc_timestamp": 1604114123775,
            "type": "update",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"b\"}"
        }
        cls.delete_diff = {
            "id": "3",
            "owner": "owner_id",
            "logical_clock": 0,
            "utc_timestamp": 1604114123776,
            "type": "delete",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\"}"
        }

    def reset_db(self):
        self.db = DataBase()
        self.db.add_table('diffs', [], UserDefinedDiff)
        self.db.add_table('model1', [], Model1)
        self.implementation = Implementation(self.db)
        self.mobync = Mobync(self.implementation)

    def create(self):
        self.mobync.synchronizer.create(self.create_diff[Diff.MODEL], self.create_diff[Diff.JSON_DATA])

        return self.mobync.synchronizer.read('model1',
                                             [ReadFilter('id', FilterType.equal, "uuid1")])

    def update(self):
        self.mobync.synchronizer.update(self.create_diff[Diff.MODEL], self.update_diff[Diff.JSON_DATA])

        return self.mobync.synchronizer.read('model1',
                                             [ReadFilter('id', FilterType.equal, "uuid1")])

    def test_01_validate_diff(self):
        with self.assertRaises(Exception):
            self.mobync._Mobync__validate_diff({})

        self.assertTrue(self.mobync._Mobync__validate_diff(self.create_diff))
        self.assertTrue(self.mobync._Mobync__validate_diff(self.update_diff))
        self.assertTrue(self.mobync._Mobync__validate_diff(self.delete_diff))

    def test_02_create_implementation(self):
        self.reset_db()
        res = self.create()
        self.assertEqual(json.loads(res)[0], json.loads(self.create_diff['json_data']))

        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [{'field1': 'a', 'id': 'uuid1'}])

    def test_03_update(self):
        self.reset_db()
        self.create()

        res = self.update()
        self.assertEqual(json.loads(res)[0], json.loads(self.update_diff['json_data']))

        pprint(json.loads(self.db.to_json()))
        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [{'field1': 'b', 'id': 'uuid1'}])

    def test_04_delete(self):
        self.reset_db()

        self.create()
        self.update()

        self.mobync.synchronizer.delete(self.create_diff[Diff.MODEL], self.delete_diff[Diff.JSON_DATA])
        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [])

    def test_05_apply_diff(self):
        self.reset_db()

        self.mobync._Mobync__apply_diff(self.create_diff)

        res = self.mobync.synchronizer.read('diffs', [ReadFilter(Diff.OWNER, FilterType.equal, "owner_id")])
        self.assertEqual(json.loads(res), [self.create_diff])

        self.assertTrue(self.mobync._Mobync__validate_diff(self.update_diff))
        self.mobync._Mobync__apply_diff(self.update_diff)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, "owner_id")])
        self.assertEqual(json.loads(res), [self.create_diff, self.update_diff])

        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [{'field1': 'b', 'id': 'uuid1'}])

        self.assertTrue(self.mobync._Mobync__validate_diff(self.delete_diff))
        self.mobync._Mobync__apply_diff(self.delete_diff)
        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, "owner_id")])
        self.assertEqual(json.loads(res), [self.create_diff, self.update_diff, self.delete_diff])
        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [])
