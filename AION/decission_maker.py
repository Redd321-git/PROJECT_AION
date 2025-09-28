from models import HealthMap
from . import factory_config
import importlib
import os

class Watcher():
	def __init__(self):
		current_dir=os.path.dirname(__file__)
		logic_dir=os.path.join(current_dir,"decision_maker_diagnostic_logics_v1")
		modules=[f[:-3] for f in os.listdir(logic_dir) if f.endswith(".py")]
		self.diagnostic_logics={}
		for m in modules:
			module=importlib.import_module(f"AION.decision_maker_diagnostic_logics_v1.{m}")
			cls=getattr(module,m)
			self.diagnostic_logics[m]=cls(factory_config)

	def permit(self,health_map: HealthMap)-> bool:
		policy_volations_detected={}
		flag=True
		for policy_name , policy in self.diagnostic_logics.items():
			result=policy.check(health_map)
			if result['violations']:
				flag=False
				health_map.problems_identified[policy_name]=result
		return flag
			
	
		