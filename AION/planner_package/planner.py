from AION.schemas import HealthMap,Query,Reason,Candidates
from rag_engine import RAG_engine
from llm_interface import LLM_interface

class Thinker():
	def __init__(self):
		self.rag=RAG_engine()
		self.llm=LLM_interface()
		
	def gen_reason(self,health_map: HealthMap) -> Reason:
		pass	
	def gen_actionset(self,query: Query) -> Candidates:
		pass
	def gen_logic(self,):
		pass