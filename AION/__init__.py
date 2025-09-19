from pathlib import Path
import joblib
from tensorflow import keras


AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"

model_version="model_v1"

model=keras.models.load_model(AION_Dependencies/model_version/"AION_RUL_prediction_model.keras")
model_input_fields=joblib.load(AION_Dependencies/model_version/"AION_RUL_predictor_features.joblib")
y_scaler=joblib.load(AION_Dependencies/model_version/"y_scaler.joblib")
x_scaler=joblib.load(AION_Dependencies/model_version/"scaler.joblib")
robot_arm_fields=joblib.load(AION_Dependencies/model_version/"AION_RUL_robot_arm_masking.joblib")
conveyor_fields=joblib.load(AION_Dependencies/model_version/"AION_RUL_conveyor_masking.joblib")

