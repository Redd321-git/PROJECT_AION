from models import State
from pathlib import Path
from tensorflow import keras
import joblib
from abc import ABC, abstractmethod
import numpy as np



class Preprocessor():
	def __init__(self,model_input_fields,x_scaler_path,conveyor_masking_path,robot_arm_masking_path):
		self.model_input_fields=model_input_fields
		self.x_scaler=joblib.load(x_scaler_path)
		self.robot_arm_fields=joblib.load(robot_arm_masking_path)
		self.conveyor_fields=joblib.load(conveyor_masking_path)
		self.machine_masking_catalog={
			'robot_arm'=[x+"_masked" for x in self.robot_arm_fields],
			'conveyor'=[y+"_masked" for y in self.conveyor_fields]
		}

	def preprocess(self,machine_type: str,machine_telemetry: dict):
		df=np.zeros((1,len(self.model_input_fields)),dtype=float)
		masking_set=set(self.machine_masking_catalog[machine_type])
		for i,field in enumerate(self.model_input_fields):
			if field in machine_telemetry:
				df[0,i]=float(machine_telemetry.get(field,0.0))
			else:
				df[0,i]=1.0 if field in masking_set else 0.0
		df_scaled=self.x_scaler.transform(df)
		return df_scaled

class Foreseer():
	def __init__(self):

		AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"

		self.model=keras.models.load_model(AION_Dependencies/"AION_RUL_prediction_model.keras")
		model_input_fields=joblib.load(AION_Dependencies/"AION_RUL_predictor_features.joblib")
		self.y_scaler=joblib.load(AION_Dependencies/"y_scaler.joblib")

		self.preprocessor=Preprocessor(
			model_input_fields,
			x_scaler_path=AION_Dependencies/"scaler.joblib",
			conveyor_masking_path=AION_Dependencies/"AION_RUL_conveyor_masking.joblib",
			robot_arm_masking_path=AION_Dependencies/"AION_RUL_robot_arm_masking.joblib"
		)

	def predict(self,state: State):
		self.machines=state.machines
		for machine in self.machines:
			machine_type=machine.get('type')
			machine_telemetry=machine.get('telemetry',{})
			processed_telemetry=self.preprocessor.preprocess(machine_type,machine_telemetry)
			rul=self.model.predict(processed_telemetry)
			scaled_rul=self.y_scaler.inverse_transform(rul)
			machine["Remaining_Unit_Lifetime"]=float(scaled_rul[0][0])
		return state


