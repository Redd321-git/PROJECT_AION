import joblib
from pathlib import Path

Base=Path(__file__).parent

model_input_fields=joblib.load(Base\"AION_RUL_predictor_features.joblib")
x_scaler=joblib.load(Base\"scaler.joblib")
machine_masking_catalog={
	MASK.stem : joblib.load(mask) for mask in (Base\mask).glob("*.joblib")
}

def preprocess(self,machine_type: str,machine_telemetry: dict):
	df=np.zeros((1,len(model_input_fields)),dtype=float)
	masking_set=set(machine_masking_catalog["AION_RUL_"+machine_type+"_masking"])
	for i,field in enumerate(model_input_fields):
		if field in machine_telemetry:
			df[0,i]=float(machine_telemetry.get(field,0.0))
		else:
			df[0,i]=1.0 if field in masking_set else 0.0
	df_scaled=x_scaler.transform(df)
	return df_scaled