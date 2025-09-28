from AION.models import HealthMap

class health_check():
	def __init__(self,factory_config : dict):
		self.baselines=factory_config['baselines']
		self.thresholds=factory_config['thresholds']

	def check(self,health_map : HealthMap):
		