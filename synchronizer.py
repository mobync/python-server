import abc


class Synchronizer(metaclass=abc.ABCMeta):

   @abc.abstractmethod
   def read(self):
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



