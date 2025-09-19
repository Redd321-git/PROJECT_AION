from models import State
from . import model, y_scaler, load_preprocessor
import numpy as np

class Foreseer():
	def __init__():
		self.preprocessor=load_preprocessor()

	def predict(self,state: State):
		self.machines=state.machines
		for machine in self.machines:
			machine_type=machine.get('type')
			machine_telemetry=machine.get('telemetry',{})
			processed_telemetry=self.preprocessor.preprocess(machine_type,machine_telemetry)
			rul=model.predict(processed_telemetry)
			scaled_rul=y_scaler.inverse_transform(rul)
			machine["Remaining_Unit_Lifetime"]=float(scaled_rul[0][0])
		return state


