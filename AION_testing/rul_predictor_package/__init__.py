from pathlib import Path
model_version="rul_model_v1"
AION_Dependency=Path(__file__).parent/model_version

from keras.models import load_model
model=load_model(filepath = AION_Dependency/"AION_RUL_prediction_model.keras",compile=False)

from joblib import load
y_scaler=load(AION_Dependency/"y_scaler.joblib")

from .rul_model_v1.preprocessor import Preprocessor
Preprocessor=Preprocessor()