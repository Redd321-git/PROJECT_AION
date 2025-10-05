from AION.models import HealthMap
from . import load_factory_config, load_runtime_logics, load_diagnostic_logics


class Watcher():
	def __init__(self):
		self.factory_config=load_factory_config()
		self.runtime_config=self.factory_config.copy()
		self.initialise_diagnostic_logics()

	def initialise_diagnostic_logics(self):
		self.runtime_logics=load_runtime_logics()
		self.diagnostic_logics=load_diagnostic_logics(self.factory_config,self.runtime_logics)
	
	def permit(self,health_map: HealthMap)-> bool:
		policy_volations_detected={}
		flag=True
		for policy_name , policy in self.diagnostic_logics.items():
			result=policy.check(health_map)
			if result.reach_out_signal['reach_out']:
				#logic for contacting the llm for logic or policy updation in the config file
			if result.violations:
				flag=False
				health_map.problems_identified[policy_name]=result
		return flag
			
	
		