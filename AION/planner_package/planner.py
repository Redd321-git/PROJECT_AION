from AION.models import HealthMap,Query,Reason
from rag_engine import RAG_engine
from llm_interface import LLM_interface

class Thinker():
	def __init__(self):
		self.rag=RAG_engine()
		self.llm=LLM_interface()
		
	def gen_reason(self,health_map: HealthMap) -> Reason:
		
	def gen_actionset(self,query: Query) -> Candidates:

	def gen_logic(self,):
		