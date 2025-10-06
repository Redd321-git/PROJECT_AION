from AION.models import HealthMap, CheckResponceSchema
from .. import eval_attr_specific, eval_hierarchical

class DataExtracter():
	def __init__(self):
		pass
	def extracte(self, health_map: Health_Map, param: dict)->float:
		
		return val

class progress_check():
	def __init__(self,factory_config : dict, runtime_logics: dict):
		self.goal_buffer={}
		self.goal_types=runtime_logics
		self.data_extracter=DataExtracter()
		
	def check(self,health_map : HealthMap)->CheckResponceSchema:
		report={}
		progress_flag=False
		for goal in health_map.goals:
			signal={}
			if goal.type not in self.goal_types:
					signal["reach_out"]=True
					signal["description"]="new goal identified"
					siganl.get("goals",{}).add(goal)
					pass
			elif goal.goal_id not in self.goal_buffer.get(goal_type,{}):
				self.goal_buffer[goal_type][goal.goal_id]=goal
		
		for goal_type,goals in self.goal_buffer.items():
			cls=self.goal_progress_check_methods[goal_type]
			body=self.goal_types[goal_type]
			params={}
			for param in cls.params:
				params[param[]]=data_extracter(param)
			eval_answer=cls.compute_func(params,goals)
			report[goal_type]=eval_answer
			progress_flag=progress_flag|eval_answer['requires_planner_action']
		return CheckResponceSchema(
				violations=progress_flag,
				report=report,
				reach_out_signal=signal
			)
		