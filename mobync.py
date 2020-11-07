import json
from typing import List

from diff import Diff, OperationType
from synchronizer import Synchronizer


class Mobync:

    diffs_model_name: str

    def __init__(self, synchronizer, diffs_model_name='diffs', user_id: str):
        if not issubclass(type(synchronizer), Synchronizer):
            Exception('synchronizer should be a subclass of Synchronizer, instead it was {}'.format(type(synchronizer)))

        self.synchronizer = synchronizer
        self.diffs_model_name = diffs_model_name

    def apply(self, logical_clock: str, diff_list: List[dict]) -> dict:

        for diff in diff_list:
            if not Diff.validate(diff):
                raise Exception('Tried to instantiate an inconsistent Diff')
            if not self.synchronizer.validate(diff):
                raise Exception('Unauthorized action by the server')

        client_last_sync_logical_clock = int(logical_clock)
        if client_last_sync_logical_clock < 0:
            raise Exception('Received an inconsistent logical clock from client: Expected and integer >= 0, received {}'.format(logical_clock))

        server_diffs = models_db.fetch_diffs(client_last_sync_logical_clock, user_id)

        diffs_to_apply_on_server = list()
        diffs_to_apply_on_client = list()
        self.__diff_treatment(diff_list, diffs_to_apply_on_server, diffs_to_apply_on_client)

        # Apply Diffs on server
        for diff in diffs_to_apply_on_server:
            self.__apply_diff(diff)

        # reply to client and client apply
        return {
            'logical_clock': logical_clock + 1,
            'diffs': diffs_to_apply_on_client,
        }

    def __apply_diff(self, diff: dict):
        if diff[Diff.TYPE] == OperationType.create:
            self.synchronizer.create(diff[Diff.MODEL], diff[Diff.JSON_DATA])
        elif diff[Diff.TYPE] == OperationType.update:
            print('') # TODO: do update
        else:
            print('') # TODO: do DELETE
        self.synchronizer.create(self.diffs_model_name, json.dumps(diff))

    def __diff_treatment(self, diff_list: List[dict], diffs_to_apply_on_server: List[dict], diffs_to_apply_on_client: List[dict]):
        # Simplify client and server with client and server DELETE diffs

        # Merge client UPDATE diffs

        # Merge client UPDATEs into client CREATEs

        # Add server CREATE diffs to apply

        # Add local  CREATE diffs to apply

        # Simplify client and server UPDATE diffs

        # Add remaining client UPDATE diffs to apply

        # Assign logical clock on diffs to apply on server
