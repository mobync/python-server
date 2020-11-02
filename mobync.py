import json
from typing import List

from diff import Diff
from synchronizer import Synchronizer


class Mobync:

    def __init__(self, synchronizer):
        if not issubclass(type(synchronizer), Synchronizer):
            Exception('synchronizer should be a subclass of Synchronizer, instead it was {}'.format(type(synchronizer)))

        self.synchronizer = synchronizer

    def apply(self, logical_clock, diff_list: List[dict]) -> dict:

        # for diff in diff_list:
        #     if not Diff.validate(diff):
        #         raise Exception('Tried to instantiate an inconsistent Diff')
        #     if not self.synchronizer.validate(diff):
        #         raise Exception('Unauthorized action by the server')

        # Sync algorithm here

        for diff in diff_list:
            self.synchronizer.create('diffs', json.dumps(diff))
            self.synchronizer.create(diff[Diff.MODEL], diff[Diff.JSON_DATA])

        return {
            'logical_clock': logical_clock + 1,
            'diffs': diff_list,
        }
