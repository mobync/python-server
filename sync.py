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
        if type(data) is dict:
            return True
        return True
