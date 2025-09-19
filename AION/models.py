from enum import Enum
from pydantic import BaseModel 
from datetime import datetime
from typing import List,Dict,Optional


class AgentState(str,Enum):
	Running="running"
	Paused="paused"
	Stopped="stopped"

class Machine(BaseModel):
	machine_id: str
	type: str
	status: str
	task: str
	telemetry: Dict[str,float]
	Remaining_Unit_Lifetime: Optional[float]=None
	
class KPI(BaseModel):
	

class Goal(BaseModel):
	goal_id: str
	description: str
	due_date: str
	priority: str
	target_quantity:Optional[int]=None
	completed_quantity: Optinal[int]=None
	baseline: Optinal[float]=None
	current: Optional[float]=None

class State(BaseModel):
	timestamp: datetime
	machines:List[machine]
	goals:List[goal]
	kpi: KPI

class HealthMap():
	
class Query():

class Reason():
	
class Candidates():
	
class ActionSet():
	