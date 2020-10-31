import abc


class Synchronizer(metaclass=abc.ABCMeta):

   @abc.abstractmethod
   def read(self, where, uuid):
      pass

   @abc.abstractmethod
   def update(self):
      pass

   @abc.abstractmethod
   def create(self):
      pass

   @abc.abstractmethod
   def delete(self):
      pass

   @abc.abstractmethod
   def validate(self):
      pass
