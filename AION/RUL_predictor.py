from models import State
from pathlib import Path
from tensorflow import keras
import joblib
from abc import ABC, abstractmethod
import pandas as pd
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

	def preprocessor(self,machine_type: str,machine_telemetry: dict):
		df=np.zeros((1,len(self.model_input_fields)),dtype=float)
		masking_set=self.machine_masking_catalog[machine_type]
		for i,field in enumerate(model_input_fields):
			if field in machine_telemetry:
				df[0,i]=machine_telemetry[field]
			else:
				df[0,i]=1.0 if field in masking_set else 0.0
		df_scaled=x_scaler.transform(df)
		return df_scaled

class Foreseer():
	def __init__(self):

		AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"

		self.model=keras.models.load_model(AION_Dependencies/"AION_RUL_prediction_model.keras")
		model_input_fields=joblib.load(AION_Dependencies/"AION_RUL_predictor_features.joblib")
		self.y_scaler=joblib.load(AION_Dependencies/"y_scaler.joblib")

		self.x_scaler_path=AION_Dependencies/"scaler.joblib"
		self.conveyor_masking_path=AION_Dependencies/"AION_RUL_conveyor_masking.joblib"
		self.robot_arm_masking_path=AION_Dependencies/"AION_RUL_robot_arm_masking.joblib"

		#self.preprocessor=Preprocessor(model_input_fields,x_scaler)

	def predict(self,state: State):
		self.machines=state.machines
		for machine in self.machines:
			processed_telemetry=preprocessor.preprocess(machine_type,machine_telemetry)
			rul=self.model.predict(processed_telemetry)
			scaled_rul=y_scaler.inverse_transform(rul)
			machine["Remaining_Unit_Lifetime"]=scaled_rul



