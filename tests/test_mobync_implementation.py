from mobync import Diff, OperationType
from mobync import Mobync
from mobync import ReadFilter, FilterType

from examples.in_memory_server_example.implementation import Implementation
from examples.in_memory_server_example.mock_data_base import DataBase
from examples.in_memory_server_example.models import Model1
import unittest


class TestSyncProtocol(unittest.TestCase):
    """
    Tests the sync protocol behavior.
    """
    @classmethod
    def setUpClass(cls):
        cls.db = DataBase()
        cls.db.add_table('diffs', [], Diff)
        cls.db.add_table('model1', [], Model1)
        cls.implementation = Implementation(cls.db)
        cls.mobync = Mobync(cls.implementation)

    def reset_db(self):
        self.db = DataBase()
        self.db.add_table('diffs', [], Diff)
        self.db.add_table('model1', [], Model1)

    def test_apply_diff(self):
        diff = {
            "id": "1",
            "owner": "owner_id",
            "logical_clock": 0,
            "utc_timestamp": 1604114123774,
            "type": OperationType.create,
            "model": "model1",
            "json_data": "{\"id\":\"uuid1\",\"field1\":\"a\"}"
        }
        self.mobync._Mobync__apply_diff(diff)

        res = self.mobync.synchronizer.read('diffs', [ReadFilter(Diff.OWNER, FilterType.equal, "owner_id")])
        print(res)
        self.assertEqual(res, [diff])
