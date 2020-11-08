import json

from mobync import Diff
from mobync import Mobync
from mobync import ReadFilter, FilterType

from examples.in_memory_server_example.implementation import Implementation
from examples.in_memory_server_example.mock_data_base import DataBase
from examples.in_memory_server_example.models import Model1, Diff as UserDefinedDiff
import unittest


class TestSyncClientIntegration(unittest.TestCase):
    """
    Tests the integration among multiple clients and one server.
    """

    @classmethod
    def setUpClass(cls):
        cls.db = DataBase()
        cls.db.add_table('diffs', [], UserDefinedDiff)
        cls.db.add_table('model1', [], Model1)
        cls.implementation = Implementation(cls.db)
        cls.mobync = Mobync(cls.implementation)

        cls.owner_id = 'asdf'
        cls.diff1 = {
            "id": "1",
            "owner": cls.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123775,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"a\"}"
        }
        cls.diff2 = {
            "id": "2",
            "owner": cls.owner_id,
            "logical_clock": 1,
            "utc_timestamp": 1604114123776,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid2\",\"field1\":\"b\"}"
        }
        cls.diff3 = {
            "id": "3",
            "owner": cls.owner_id,
            "logical_clock": 0,
            "utc_timestamp": 1604114123777,
            "type": "create",
            "model": "model1",
            "json_data": "{\"id\":\"uuid3\",\"field1\":\"c\"}"
        }
        cls.diff4 = {
            "id": "4",
            "owner": cls.owner_id,
            "logical_clock": 3,
            "utc_timestamp": 1604114123778,
            "type": "update",
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"x\"}"
        }
        cls.diff5 = {
            "id": "5",
            "owner": cls.owner_id,
            "logical_clock": 4,
            "utc_timestamp": 1604114123779,
            "type": "delete",
            "model": "model1",
            "json_data": "{\"id\":\"uuid3\"}"
        }

        cls.client = {
            "client_1": {
                "diffs": [],
                "logical_clock": 0
            },
            "client_2": {
                "diffs": [],
                "logical_clock": 0
            }
        }

    def merge_response_to_client_data(self, client: str, res: dict):
        self.client[client]["logical_clock"] = res["logical_clock"]
        self.client[client]["diffs"] = self.client[client]["diffs"] + res["diffs"]

    def merge_diffs_into_client_data(self, client: str, diffs: list):
        self.client[client]["diffs"] = self.client[client]["diffs"] + diffs

    def test_01_client_1_creates_local_object_and_synchronizes(self):
        self.merge_diffs_into_client_data("client_1", [self.diff1])
        data = {
            "logical_clock": self.client["client_1"]["logical_clock"],
            "diffs": [self.diff1]
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 1, "diffs": [], "success": True, "message": ""})
        self.merge_response_to_client_data("client_1", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1])

    def test_02_client_1_and_2_create_local_objects_but_neither_synchronizes(self):
        self.merge_diffs_into_client_data("client_1", [self.diff2])
        self.merge_diffs_into_client_data("client_2", [self.diff3])

    def test_03_client_2_synchronizes(self):
        data = {
            "logical_clock": self.client["client_2"]["logical_clock"],
            "diffs": [self.diff3]
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 2, "diffs": [self.diff1], "success": True, "message": ""})
        self.merge_response_to_client_data("client_2", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1, self.diff3])

    def test_04_client_1_synchronizes(self):
        data = {
            "logical_clock": self.client["client_1"]["logical_clock"],
            "diffs": [self.diff2]
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 3, "diffs": [self.diff3], "success": True, "message": ""})
        self.merge_response_to_client_data("client_1", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1, self.diff3, self.diff2])

    def test_05_client_2_synchronizes(self):
        data = {
            "logical_clock": self.client["client_2"]["logical_clock"],
            "diffs": []
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 3, "diffs": [self.diff2], "success": True, "message": ""})
        self.merge_response_to_client_data("client_2", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1, self.diff3, self.diff2])

    def test_06_client_2_updates_client_1_object_and_both_synchronizes(self):
        self.merge_diffs_into_client_data("client_2", [self.diff4])
        data = {
            "logical_clock": self.client["client_2"]["logical_clock"],
            "diffs": [self.diff4]
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 4, "diffs": [], "success": True, "message": ""})
        self.merge_response_to_client_data("client_2", res)

        data = {
            "logical_clock": self.client["client_1"]["logical_clock"],
            "diffs": []
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 4, "diffs": [self.diff4], "success": True, "message": ""})
        self.merge_response_to_client_data("client_1", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1, self.diff3, self.diff2, self.diff4])

    def test_07_client_1_deletes_client_2_and_both_synchronizes(self):
        self.merge_diffs_into_client_data("client_1", [self.diff5])
        data = {
            "logical_clock": self.client["client_1"]["logical_clock"],
            "diffs": [self.diff5]
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 5, "diffs": [], "success": True, "message": ""})
        self.merge_response_to_client_data("client_1", res)

        data = {
            "logical_clock": self.client["client_2"]["logical_clock"],
            "diffs": []
        }
        res = self.mobync.apply(data["logical_clock"], data["diffs"], self.owner_id)
        self.assertEqual(res, {"logical_clock": 5, "diffs": [self.diff5], "success": True, "message": ""})
        self.merge_response_to_client_data("client_2", res)

        res = self.mobync.synchronizer.read("diffs", [ReadFilter(Diff.OWNER, FilterType.equal, self.owner_id)])
        self.assertEqual(json.loads(res), [self.diff1, self.diff3, self.diff2, self.diff4, self.diff5])

    def test_08_database_check(self):
        res = self.mobync.synchronizer.read("model1", [])
        self.assertEqual(json.loads(res), [{'id': 'uuid1', 'field1': 'x'},
                                           {'id': 'uuid2', 'field1': 'b'}])


if __name__ == '__main__':
    unittest.main()
