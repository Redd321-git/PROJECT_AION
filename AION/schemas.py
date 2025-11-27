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
	heath_report: Optional[Dict]=None
	
class KPI(BaseModel):
	

class Goal(BaseModel):
	goal_id: str
	description: str
	goal_type: str
	due_date: str
	priority: str
	target_quantity:Optional[int]=None
	completed_quantity: Optional[int]=None
	baseline: Optional[float]=None
	current: Optional[float]=None

class State(BaseModel):
	timestamp: datetime
	machines:List[Machine]
	goals:List[Goal]
	kpi: KPI

class HealthMap(State):
	problems_identified:Optional[dict]=None
	factor_health:Optional[str]=None

class CheckResponceSchema(BaseModel):

class Query():

class Reason():
	
class Candidates():
	
class ActionSet():
	
class UserResponse(BaseModel):

class UserCreate(BaseModel):

class CheckResponceSchema(BaseModel):
