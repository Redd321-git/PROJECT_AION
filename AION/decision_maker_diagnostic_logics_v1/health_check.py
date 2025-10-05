from AION.models import HealthMap,CheckResponceSchema

def eval_health_attr_specific(val,condition,crit_threshold,warn_threshold):
	if condition in ["<","<="]:
		if val<crit_threshold:
			return "critical"
		elif val<warn_threshold:
			return "warning"
		else:
			return "healthy"

	elif condition in [">",">="]:
		if val>crit_threshold:
			return "critical"
		elif val>warn_threshold:
			return "warning"
		else:
			return "healthy"
	else:
		raise ValueError(f"unknown condition: {condition}")

def eval_health_hierarchical(health_score:dict,warn_count_threshold:int):
	warn_count=0
	for attr, cat in health_score.items():
		if cat=="critical":
			return "critical"
		if cat=="warning":
			warn_count+=1
	if warn_count>warn_count_threshold:
		 return "critical"
	if warn_count<=1:
		return "healthy"
	return "warning"
		

class health_check():
	def __init__(self,factory_config : dict, runtime_logics : dict):
		self.baselines=factory_config["baselines"]
		self.thresholds=factory_config["thresholds"]
		self.warn_count_threshold=factory_config["warn_count_threshold"]

	def check(self,health_map : HealthMap)->CheckResponceSchema:
		health_scores_per_machine={}
		health_flag=False
		for machine in health_map.machines:
			health_score={}
			for attr,policy in self.thresholds[machine.machine_type].items():
				health_score[attr]=eval_health_attr_specific(
					machine.telemetry[attr],
					policy['condition'],
					policy['crit_threshold'],
					policy['warn_threshold']
				)
			health_score["health_summary"]=eval_health_hierarchical(health_score,self.warn_count_threshold)
			health_scores_per_machine[machine.machine_id]=health_score["health_summary"]
			machine.health_report=health_score
		health_map.factory_health=eval_health_hierarchical(health_scores_per_machine,self.warn_count_threshold)
		health_flag=health_map.factory_health!="healthy"
		return CheckResponceSchema(
				violations=health_flag,
				report={"health report per machine":health_scores_per_machine},
				reach_out_signal={signal["reach_out"]:True}
			)