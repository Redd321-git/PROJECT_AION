from models import State
from AION import model, model_input_fields, y_scaler,x_scaler,robot_arm_fields,conveyor_arm_fields
import numpy as np



class Preprocessor():
	def __init__(self):
		model_input_fields=model_input_fields
		
		self.machine_masking_catalog={
			'robot_arm'=[x+"_masked" for x in robot_arm_fields],
			'conveyor'=[y+"_masked" for y in conveyor_fields]
		}

	def preprocess(self,machine_type: str,machine_telemetry: dict):
		df=np.zeros((1,len(model_input_fields)),dtype=float)
		masking_set=set(self.machine_masking_catalog[machine_type])
		for i,field in enumerate(model_input_fields):
			if field in machine_telemetry:
				df[0,i]=float(machine_telemetry.get(field,0.0))
			else:
				df[0,i]=1.0 if field in masking_set else 0.0
		df_scaled=x_scaler.transform(df)
		return df_scaled

class Foreseer():
	def __init__(self):
		
		self.preprocessor=Preprocessor()

	def predict(self,state: State):
		self.machines=state.machines
		for machine in self.machines:
			machine_type=machine.get('type')
			machine_telemetry=machine.get('telemetry',{})
			processed_telemetry=self.preprocessor.preprocess(machine_type,machine_telemetry)
			rul=model.predict(processed_telemetry)
			scaled_rul=self.y_scaler.inverse_transform(rul)
			machine["Remaining_Unit_Lifetime"]=float(scaled_rul[0][0])
		return state


