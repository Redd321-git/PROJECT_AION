from queue import Queue

class bottleneck_check():
	def __init__(self,factory_graph: dict):
		self.start_nodes=factory_graph['roots']
		self.edges=factory_graph['edges']
		self.machines=factory_graph['machines']
		self.in_rate={m_id : 0 for m_id in self.machines}
		self.in_degree={m_id : 0 for m_id in self.machines}
		for parent, children in self.edges.items():
			for child in children:
				self.in_degree[child]+=1

		
	def check(self,current_processing_power: dict ,product_flow_ratio: dict):

		self.bottle_necks=[]
		self.pro_cap=current_processing_power
		self.prd_fl_rtio=product_flow_ratio
		self.q=Queue()
		in_deg_copy=self.in_degree.copy()

		for root in self.start_nodes:
			self.in_rate[root]=self.pro_cap.get(root,0)
			self.q.put(root)

		while not self.q.empty():

			parent=self.q.get()
			for child in self.edges.get(parent,[]):

				self.in_rate[child]+=min(self.pro_cap.get(parent,0),self.in_rate.get(parent,0))*self.prd_fl_rtio.get(parent,{}).get(child,0)
				in_deg_copy[child]-=1

				if in_deg_copy.get(child)==0 :
					self.q.put(child)

		for m_id , in_q in self.in_rate.items():

			if in_q > self.pro_cap.get(m_id,0):
				self.bottle_necks.append(m_id)

		return self.bottle_necks
				
			