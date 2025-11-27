from joblib import load
from pathlib import Path
import numpy as np

class Preprocessor():
	def __init__(self):
		Base=Path(__file__).parent

		self.model_input_fields=load(Base/"AION_RUL_predictor_features.joblib")
		self.x_scaler=load(Base/"scaler.joblib")
		self.machine_masking_catalog={
			mask.stem : load(mask) for mask in (Base/"mask").glob("*.joblib")
		}
		self.ft_names=self.x_scaler.get_feature_names_out()
		self.idx_map={fld:i for i,fld in enumerate(self.model_input_fields)}

	def preprocess(self,machine_type: str,machine_telemetry: dict):
		df_masked=np.zeros((1,len(self.model_input_fields)),dtype=float)
		masking_set=set(self.machine_masking_catalog["AION_RUL_"+machine_type+"_masking"])
		df=[[float(machine_telemetry.get(ft,0.0)) for ft in self.ft_names]]
		df_scaled=self.x_scaler.transform(df)
		for i,field in enumerate(self.ft_names):
			if field in machine_telemetry:
				df_masked[0,self.idx_map.get(field)]=df_scaled[0,i]
			else:
				msk_fld=field+'_masked'
				df_masked[0,self.idx_map.get(msk_fld)]=1.0 if msk_fld not in masking_set else 0.0
		return df_masked