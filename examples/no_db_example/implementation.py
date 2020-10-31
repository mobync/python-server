from synchronizer import Synchronizer


class Implementation(Synchronizer):

    def __init__(self, db):
        self.db = db

    def read(self, where, uuid):
        if where in self.db:
            return self.db[where]

    def update(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass

    def validate(self):
        pass
