from AION.schemas import State
from . import model, y_scaler, Preprocessor

class Foreseer():
	def __init__(self):
		self.preprocessor=Preprocessor
		
	def predict(self,state: State):
		self.machines=state['machines']
		for machines_id,machine in self.machines.items():
			print(machines_id)
			machine_type=machine.get('type')
			machine_telemetry=machine.get('telemetry',{})
			processed_telemetry=self.preprocessor.preprocess(machine_type,machine_telemetry)
			rul=model.predict(processed_telemetry)
			scaled_rul=rul
			machine["Remaining_Unit_Lifetime"]=float(scaled_rul[0][0])
		return state
	
def test_rul_predictor():
	frsr=Foreseer()
	state={
		"machines":{
			"machine_1":{
				"machine_id":"machine_1",
				"type":"conveyor",
				"telemetry":{
					'cycle':2,
					'external_load':48.21969696,
					'operational_mode':0,
					'maintainance_flag':0,
					'motor_current':11.91321482,
					'motor_voltage':219.7114193,
					'vibration_rms':0.038478776,
					'angular_velocity':0.991617041
				}
			},
			"machine_2":{
				"machine_id":"machine_2",
				"type":"robot_arm",
				"telemetry":{
					'cycle':348,																			
					'operation_mode':1,
					'maintenance_flag':0,
					'external_load':28.46552453,
					'motor_current_joint1':	5.914026626,
					'motor_voltage_joint1':	31.35865614,
					'torque_command_joint1':	15.03226525,
					'torque_measured_joint1':	14.90673726,
					'joint_position_error1'	:-0.008621808,
					'joint_temperature1'	:33.30396924,
					'vibration_rms1'	:0.014281488,
					'motor_current_joint2':	5.656467645,
					'motor_voltage_joint2':	31.28731283,	
					'torque_command_joint2':	14.0945923,
					'torque_measured_joint2':	13.45530105,
					'joint_position_error2'	:-0.020494702,
					'joint_temperature2'	:33.01204899,
					'vibration_rms2'	:0.016169153,
					'motor_current_joint3':	6.312187226,
					'motor_voltage_joint3':	30.66602929,
					'torque_command_joint3':13.97100158,
					'torque_measured_joint3'	:13.99481042,
					'joint_position_error3'	:-0.012493978,
					'joint_temperature3'	:31.10624044,	
					'vibration_rms3':0.02596622,
				}
			}
		}
	}
	health_map=frsr.predict(state)
	print(health_map)