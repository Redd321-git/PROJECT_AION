from AION.models import HealthMap, CheckResponceSchema
from .. import eval_attr_specific, eval_hierarchical
from statistics import mean
import re

aggregate_types={
	"sum":sum,
	"mean":mean,
	"max":max,
	"min":min,
	"len":len,
}

class DataExtracter():
	def __init__(self):
		self.custom_logics={}

	def extract(self, health_map: HealthMap, params: list)->dict:
		results={}
		for param in params:
			parts=param["path"].split('.')
			raw=self.fetch(obj=health_map,parts,idx=0)
			flat=self.flatten(raw)
			results[param["name"]]=self.aggregate_func(flat,param['aggregate'])
		return results

	def fetch(self, obj, parts:list , idx:int)->list:
		if idx>=len(parts): 
			return [obj] if not isinstance(obj,list) else obj
		part=parts[idx]
		if part=="*":
			res=[]
			if isinstance(obj, dict):
				for key in obj:
					res.extend(self.fetch(obj[key],parts,idx+1))
			elif isinstance(obj,list):
				for item in obj:	
					res.extend(self.fetch(item,parts,idx+1))
			return res
		elif part.startswith('[') and part.endswith(']'):
			keys=re.findall(r"[^\[\],]+",part)
			res=[]
			for key in keys:
				if isinstance(obj, dict) and key in obj:
					res.extend(self.fetch(obj[key],parts,idx+1))
			return res
		else:
			next_obj=None
			if isinstance(obj, dict) and part in obj:
				next_obj=obj[part]
			elif hasattr(obj,part):
				next_obj=getattr(obj,part)
			else :
				return []
			return self.fetch(next_obj,parts,idx+1)

	def flatten(self,lst: list)->list:
		result=[]
		for item in lst:
			if isinstance(item,list):
				result.extend(self.flatten(item))
			else:
				result.append(item)
		return result	
			
	def aggregate_func(self,flat: list,aggregate: str):
		if aggregate in {"sum","mean","max","min"}:
			func=getattr(self,f"agg_{aggregate}")
			return func(flat)
		if aggregate not in self.custom_logics:
			try:
				self.custom_logics[aggregate]=eval(aggregate,{"__builtins__":None},aggregate_types)
			except Exception as e:
				raise ValueError(f"invalid custom logic aggregate: {e}")
		return self.custom_logics[aggregate](flat)

	def agg_sum(self,vals: list)->float:
		return sum(vals)
	def agg_min(self,vals: list)->float:
		return min(vals) if vals else None
	def agg_max(self,vals: list)->float:
		return max(vals) if vals else None
	def agg_mean(self,vals: list)->float:
		return mean(vals) if vals else 0
	
		
		
class progress_check():
	def __init__(self,factory_config : dict, runtime_logics: dict):
		self.goal_buffer={}
		self.goal_progress_check_methods=runtime_logics
		self.data_extracter=DataExtracter()
		
	def check(self,health_map : HealthMap)->CheckResponceSchema:
		report={}
		progress_flag=False
		signal={"reach_out": False, "description": "", "goals": []}
		for goal in health_map.goals.values():
			goal_type=goal.goal_type
			if goal_type not in self.goal_progress_check_methods:
				signal["reach_out"]=True
				signal["description"]="new goal identified"
				signal["goals"].append(goal)
				continue

			if goal_type not in self.goal_buffer:
				self.goal_buffer[goal_type]={}
			if goal.goal_id not in self.goal_buffer.get(goal_type,{}):
				self.goal_buffer[goal_type][goal.goal_id]=goal
		
		for goal_type,goals in self.goal_buffer.items():
			cls=self.goal_progress_check_methods[goal_type]
			params=self.data_extracter.extract(health_map, cls.params)
			eval_answer=cls.compute_func(params,goals)
			report[goal_type]=eval_answer
			if eval_answer.get('requires_planner_action',False):
				progress_flag=True

		return CheckResponceSchema(
				violations=progress_flag,
				report=report,
				reach_out_signal=signal
			)
		