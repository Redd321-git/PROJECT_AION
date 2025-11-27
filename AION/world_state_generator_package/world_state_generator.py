from AION.schemas import State
from env_interfaces import Environment

class Eye:
	def __init__(self,env: Environment):
		self.world=env
		
	def observe(self) -> State:
		return self.world.get_state()
		


def KPI_compute(state : State):
	kpi={
	}
	return kpi