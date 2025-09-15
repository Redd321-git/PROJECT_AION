from abc import ABC, abstractmethod
from typing import Any
class Environment(ABC):

	@abstractmethod
	def connect(self):
		pass

	@abstractmethod
	def disconnect(self):
		pass

	@abstractmethod
	def reset(self):
		pass

	@abstractmethod
	def step(self,action: Any):
		pass

	@abstractmethod
	def get_state(self):
		pass

	@abstractmethod
	def send_command(self,command:str):
		pass
	