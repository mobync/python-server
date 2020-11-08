import json
from typing import List

from diff import Diff, OperationType
from read_filter import ReadFilter, FilterType
from synchronizer import Synchronizer


class Mobync:
    synchronizer: Synchronizer
    diffs_model_name: str
    diffs_model_name: str
    server_diffs: List[dict]
    client_diffs: List[dict]
    diffs_to_apply_on_server: List[dict]
    diffs_to_apply_on_client: List[dict]

    def __init__(self, synchronizer: Synchronizer, diffs_model_name='diffs'):
        if not issubclass(type(synchronizer), Synchronizer):
            Exception('synchronizer should be a subclass of Synchronizer, instead it was {}'.format(type(synchronizer)))

        self.synchronizer = synchronizer
        self.diffs_model_name = diffs_model_name

    def apply(self, logical_clock: str, diff_list: List[dict], owner_id: str) -> dict:

        for diff in diff_list:
            if not Diff.validate(diff):
                raise Exception('Tried to instantiate an inconsistent Diff')
            if not self.synchronizer.validate(json.dumps(diff)):
                raise Exception('Unauthorized action by the server')

        client_last_sync_logical_clock = int(logical_clock)
        if client_last_sync_logical_clock < 0:
            raise Exception(
                'Received an inconsistent logical clock from client: Expected and integer >= 0, received {}'.format(
                    logical_clock))

        a = self.synchronizer.read(self.diffs_model_name,
                                                   [ReadFilter(Diff.OWNER, FilterType.equal, owner_id),
                                                    ReadFilter(Diff.LOGICAL_CLOCK, FilterType.majorOrEqual,
                                                               client_last_sync_logical_clock)])
        self.server_diffs = json.loads(a)



        # TODO: change this
        all_server_diffs = self.synchronizer.read(self.diffs_model_name,
                                                  [ReadFilter(Diff.OWNER, FilterType.equal, owner_id)])
        all_server_diffs = json.loads(all_server_diffs)

        if all_server_diffs:
            self.logical_clock = max([diff[Diff.LOGICAL_CLOCK] for diff in all_server_diffs])
        else:
            self.logical_clock = -1



        self.client_diffs = diff_list

        self.diffs_to_apply_on_server = list()
        self.diffs_to_apply_on_client = list()

        # TODO: change this
        # self.__diff_treatment()
        # self.state_changed = False
        self.__mock_diff_treatment()

        # Apply Diffs on server
        for diff in self.diffs_to_apply_on_server:
            self.__apply_diff(diff)

        # if self.state_changed:
        #     return_logical_clock = self.logical_clock + 1
        # else:
        #     return_logical_clock = self.logical_clock



        # TODO: change this
        all_server_diffs = self.synchronizer.read(self.diffs_model_name,
                                                  [ReadFilter(Diff.OWNER, FilterType.equal, owner_id)])
        all_server_diffs = json.loads(all_server_diffs)

        if all_server_diffs:
            self.logical_clock = max([diff[Diff.LOGICAL_CLOCK] for diff in all_server_diffs])
        else:
            self.logical_clock = -1



        # reply to client and client apply
        return {
            'success': True,
            'message': '',
            # 'logical_clock': str(client_last_sync_logical_clock + 1),
            # 'logical_clock': return_logical_clock,
            'logical_clock': self.logical_clock + 1,
            # 'diffs': self.diffs_to_apply_on_client,
            'diffs': self.server_diffs,  # TODO: change this
        }

    def __apply_diff(self, diff: dict):
        if diff[Diff.TYPE] == OperationType.create:
            self.synchronizer.create(diff[Diff.MODEL], diff[Diff.JSON_DATA])
        elif diff[Diff.TYPE] == OperationType.update:
            print('')  # TODO: do update
        else:
            print('')  # TODO: do DELETE
        self.synchronizer.create(self.diffs_model_name, json.dumps(diff))

    def __mock_diff_treatment(self):
        for diff in self.client_diffs:
            # self.state_changed = True
            diff[Diff.LOGICAL_CLOCK] = self.logical_clock + 1
            self.synchronizer.create(self.diffs_model_name, json.dumps(diff))

    def __diff_treatment(self):
        self.__simplify_server_and_client_diffs_with_delete_diffs()
        self.__merge_client_update_diffs()
        self.__merge_client_updates_into_client_creates()

        # 4. Add server CREATE diffs to apply

        # 5. Add local  CREATE diffs to apply

        # 6. Simplify client and server UPDATE diffs

        # 7. Add remaining client UPDATE diffs to apply

        # 8. Assign logical clock on diffs to apply on server

    def __simplify_server_and_client_diffs_with_delete_diffs(self) -> None:
        # 1.
        pass

    def __merge_client_update_diffs(self):
        # 2. Merge client UPDATE diffs
        pass

    def __merge_client_updates_into_client_creates(self):
        # 3. Merge client UPDATEs into client CREATEs
        pass

    def __add_server_create_diffs_to_apply_on_client(self):
        # 4. Add server CREATE diffs to apply on client
        pass

    def __add_local_create_diffs_to_apply(self):
        # 5. Add local CREATE diffs to apply
        pass
