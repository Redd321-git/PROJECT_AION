from typing import Optional
from multiprocessing import Process, Queue, Event
import time

from env_interfaces import Environment
from models import AgentState

from world_state_generator import Eye, KPI_compute
from RUL_predictor import Foreseer
from decission_maker import Watcher
from planner import Thinker
from action_space import Pruner
from rl_scorer import ViceOne
from validation_layer import Validator
from communication_layer import Voice
from action_performer import Automaton
from critic import Muse

class AION:
	def __init__(self,env: Environment):

		self.aion_state: AgentState = AgentState.Stopped
		self.world: Optional[Environment]=None

		self.state_q=Queue(maxsize=1)		# queue for the world states the states will be offered by Eye and will be polled by Foreseer
		self.plan_q=Queue(maxsize=2)
		self.candidate_q=Queue(maxsize=2)
		self.action_q=Queue(maxsize=6)		# queue for action that might or are needed to be performed offered by Validator and Automanton
		self.reason_q=Queue(maxsize=10)		# queue for communincation between Voice, Watcher and Thinker
		self.in_q=Queue(maxsize=20)
		self.out_q=Queue(maxsize=20)
		self.feedback_q=Queue(maxsize=5)	# queue for letting Muse know the actions performed offereb by muse and polled by Automaton 
		self.kpi_q=Queue(maxsize=5)		# queue for KPI sharing offered by Eye and polled by Muse 
		
		self.eye=Eye(world)
		self.foreseer=Foreseer()
		self.watcher=Watcher()
		self.thinker=Thinker()
		self.pruner=Pruner()
		self.viceone=ViceOne()
		self.validator=Validator()
		self.voice=Voice()
		self.automaton=Automaton()
		self.muse=Muse()

		self.stop_event=Event()
		self.paused_event=Event()
		self.processes=[]
		
	def run_eye(self):
		while not self.stop_event.is_set():
			state=self.eye.observe()
			kpi=KPI_compute(state)
			self.kpi_q.put((time.time(),kpi))
			self.state_q.put((state,kpi))
			time.sleep(3)
			
	def run_thinker(self):
		while not self.stop_event.is_set():
			if not self.paused_event.is_set():
				if not self.reson_q.empty():
					query=self.reson_q.get()
					reason=self.thinker.reason(query)
					self.in_q.put(reason)
				if not self.plan_q.empty():
					query=self.plan_q.get()
					candidates=self.thinker.plan(query)
					self.candidate_q.put(candidates)
				time.sleep(0.1)
	
	def run_vocie(self):
		routes={
			"action":self.out_q,
			"operator":self.out_q,
			"reason":self.reason_q,
			"error":self.out_q,
			"status":self.out_q
		}
		while not self.stop_event.is_set():
			if not self.in_q.empty():
				query=self.in_q.get()
				query_type=self.voice.get_query_type(query)
				t_q=routes.get(query_type)
				if t_q:
					t_q.put(query)
				else:
					self.out_q.put({
						"type":"error",
						"payload"={
							"msg":"unknown query",
							"query":query
						}
					})
			time.sleep(0.1)
				
	
	def step(self):
		while not self.stop_event.is_set():
			try:
				state,kpi=self.state_q.get(timeout=1)
			except queue.Empty:
				continue

			health_map=self.forseer.predict(state)

			if not self.watcher.permit(health_map):
				self.in_q.put({
					"type":"status",
					"payload":{
						"msg":"Watcher found healty state"
					}
				})
				continue

			if self.paused_event.is_set():
				self.in_q.put({
					"type":"status",
					"payload":{
						"msg":"Watcher found unhealthy state, AION in paused state"}
					}
				})
				continue

			self.plan_q.put(health_map)

			try:
				candidates=self.candidate_q.get(timeout=2)
			except queue.Empty:
				continue

			feasible=self.pruner.prune(candidates)
			action=self.ViceOne.choose(feasible)

			if not self.validator.validate(action,health_map):
				self.in_q.put({
					"type":"status",
					
					"msg":"Validator rejected the action",
					"action":action
				})
				continue

			payload={
				"type":"action",
				"action":action,
				"health_map":health_map
			}
			self.in_q.put(payload)
			self.action_q.put((action.state,kpi))

	def run_automaton(self):
		while not self.stop_event.is_set():
			if self.paused_event.is_set():
				continue
			try:
				action,state,kpi=self.action_q.get(timeout=0.1)		
			except queue.Empty:
				continue

			if self.automaton.perform(action):
				self.feedback_q.put((action,state,kpi))
			else: 
				self.in_q.put({
					"type":"status",
					"payload":{
						"msg":"Automaton failed to excute the action",
						"action":action
					}
				})
				continue
				
	
	def run_muse(self):
		while not self.stop_event.is_set():
			if not self.paused_event.is_set():
				if not self.feedback_q.empty():
					action, state, kpi=self.feedback_q.get()
					self.muse.reflect_action(action,state,kpi)

				if not self.kpi_q.empty():
					kpi_time,kpi_now=self.kpi_q.get()
					self.muse.reflect_kpi(kpi_time,kpi_now)
			time.sleep(0.1)

	def start(self):
		self.aion_state=AgentState.Running
		self.stop_event.clear()
		self.processes=[
			Process(target=run_eye),
			Process(target=run_thinker),
			Process(target=run_voice),
			Process(target=step),
			Process(target=run_automton),
			Process(target=run_muse)
		]
		for p in self.processes:
			p.start()

	def paused(self):
		if self.aion_state==AgentState.Running:
			self.aion_state=AgentState.Paused
			self.paused_event.set()
	
	def resume(self):
		if self.aion_state==AgentState.Paused:
			self.aion_state=AgentState.Running
			self.paused_event.clear()
	
	def stop(self):
		self.aion_state=AgentState.Stopped
		self.stop_event.set()
		for p in self.processes:
			p.terminate()
			p.join()
			
		