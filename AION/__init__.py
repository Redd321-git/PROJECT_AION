from pathlib import Path
import joblib
import importlib.util
from tensorflow import keras


AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"

model_version="model_v1"

model=keras.models.load_model(AION_Dependencies/model_version/"AION_RUL_prediction_model.keras")
y_scaler=joblib.load(AION_Dependencies/model_version/"y_scaler.joblib")

def load_preprocessor():
	spec=importlib.util.spec_from_location("preprocessor",AION_Dependencies/model_version/"preprocessor.py")
	module=importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module.Preprocessor()



