from queue import Queue
from AION.models import HealthMap,Check_responce_schema

class coordination_check():
	def __init__(self,factory_config : dict):
		
		self.start_nodes=factory_config['factory_graph']['roots']
		self.edges=factory_config['factory_graph']['edges']
		self.machines=factory_config['machines']
		self.in_degree={m_id : 0 for m_id,mtype in self.machines.items()}
		for parent, children in self.edges.items():
			for child in children:
				self.in_degree[child]+=1

		
	def check(self,health_map : HealthMap)->Check_responce_schema:
		current_processing_power=health_map.current_processing_power
		product_flow_ratio=health_map.product_flow_ratio
		in_rate={m_id : 0 for m_id,m_type in self.machines.items()}
		queue=Queue()
		in_deg_copy=self.in_degree.copy()

		for root in self.start_nodes:
			in_rate[root]=current_processing_power.get(root,0)
			queue.put(root)

		while not queue.empty():
			parent=queue.get()
			parent_rate=min(current_processing_power.get(parent,0),in_rate.get(parent,0))
			for child in self.edges.get(parent,[]):
				in_rate[child]+=parent_rate*product_flow_ratio.get(parent,{}).get(child,0)
				in_deg_copy[child]-=1
				if in_deg_copy.get(child)==0 :
					queue.put(child)
		
		bottle_necks=[
			m_id for m_id , rate in in_rate.items()
			if rate > current_processing_power.get(m_id,0)
		}

		return {'violations':bool(bottle_necks),'bottle necks':bottle_necks}
				
			