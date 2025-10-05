from models import HealthMap
from . import load_factory_config, load_runtime_logics
import importlib
import os

class Watcher():
	def __init__(self):
		self.factory_config=load_factory_config()
		self.runtime_config=self.factory_config.copy()
		self.load_diagnostic_logics()

	def load_diagnostic_logics():
		self.runtime_logics=load_runtime_logics()
		current_dir=os.path.dirname(__file__)
		logic_dir=os.path.join(current_dir,"decision_maker_diagnostic_logics_v1")
		modules=[f[:-3] for f in os.listdir(logic_dir) if f.endswith(".py")]
		self.diagnostic_logics={}
		for m in modules:
			module=importlib.import_module(f"AION.decision_maker_diagnostic_logics_v1.{m}")
			cls=getattr(module,m)
			self.diagnostic_logics[m]=cls(self.factory_config,self.runtime_logics)
	
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
			
	
		