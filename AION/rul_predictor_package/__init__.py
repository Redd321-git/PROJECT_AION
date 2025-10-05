from pathlib import Path
import joblib
import importlib.util
from tensorflow import keras

model_version="rul_model_v1"

AION_Dependency=Path(__file__).parent/model_version

model=keras.models.load_model(AION_Dependency/"AION_RUL_prediction_model.keras")
y_scaler=joblib.load(AION_Dependency/"y_scaler.joblib")

spec=importlib.util.spec_from_location("preprocessor",AION_Dependency/"preprocessor.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Preprocessor=module.Preprocessor