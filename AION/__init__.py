from pathlib import Path
import joblib
import importlib.util
from tensorflow import keras
import json

AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"
AION_Runtime=Path(__file__).resolve().parents[1]/"AION_rutime"

model_version="rul_model_v1"
#diagnotic_logics_version="decision_maker_diagnostic_logics_v1"


model=keras.models.load_model(AION_Dependencies/model_version/"AION_RUL_prediction_model.keras")
y_scaler=joblib.load(AION_Dependencies/model_version/"y_scaler.joblib")

def load_preprocessor():
	spec=importlib.util.spec_from_location("preprocessor",AION_Dependencies/model_version/"preprocessor.py")
	module=importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.Preprocessor()

def load_factory_config():
	with open(AION_Dependencies/"factory_policy_config.json",'r') as f:
		factory_config=json.load(f)
	return factory_config

def load_runtime_logics():
	modules=[f.stem for f in AION_Runtime.iterdir() if f.endswith(".py") and f.name!="__init__.py"]
	runtime_logics={}
	for m in modules:
		module=importlib.import_module(f"AION_Runtime.{m}")
		cls=getattr(module,m)
		runtime_logics[m]=cls()
	return runtime_logics