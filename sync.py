from synchronizer import Synchronizer


class Sync:

    def __init__(self, synchronizer):
        if not issubclass(type(synchronizer), Synchronizer):
            Exception('synchronizer should be a subclass of Synchronizer, instead it was {}'.format(type(synchronizer)))

        self.synchronizer = synchronizer

    def apply(self, data):
        # Develop the diffs merge and apply algorithm
        return {}

    def is_valid(self, data):
        # Verify if the diff format is correct

        def validate_id(id):
            return bool(id)

        def validate_owner(owner):
            return

        def validate_upstream_height(upstream_height):
            return type(upstream_height) == int and upstream_height >= 0

        def validate_timestamp(timestamp):
            return type(timestamp) == int and timestamp >= 0

        # def validate_operation_type(operation_type):

        if type(data) is dict:
            return True
        return True
