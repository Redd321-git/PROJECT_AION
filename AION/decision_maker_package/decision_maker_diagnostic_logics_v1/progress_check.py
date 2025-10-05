from AION.models import HealthMap, CheckResponceSchema

class progress_check():
	def __init__(self,factory_config : dict, runtime_logics: dict):
		self.goal_buffer={}
		self.goal_types=runtime_logics
		
	def check(self,health_map : HealthMap)->CheckResponceSchema:
		for goal in health_map.goals:
			signal={}
			if goal.goal_id not in self.goal_buffer:
				if goal.type not in self.goal_types:
					signal["reach_out"]=True
					signal["description"]="new goal identified"
					siganl.get("goals",{}).add(goal)
					pass
				self.goal_buffer[goal.goal_id]=goal

		for goal_id,goal in self.goal_buffer.items():
			compute_func=self.goal_progress_check_methods[goal.goal_type]
			body=self.goal_types[goal.goal_type]
			params={}
			# retrival and processing of specified params from the health map and store it in the dict params
			eval_answer=compute_func(params)
			
		return CheckResponceSchema(
				violations=,
				report=,
				reach_out_signal=signal
			)
		