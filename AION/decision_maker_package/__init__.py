from pathlib import Path
import joblib
import importlib.util
from tensorflow import keras
import json

from AION import load_factory_config , load_runtime_logics

logics_version="decision_maker_diagnostic_logics_v1"

AION_Root=Path(__file__).resolve().parents[2]
AION_Dependencies=AION_Root/"AION_dependencies"
AION_Runtime=AION_Root/"AION_runtime"
logic_dir=Path(__file__).parent/logics_version

def load_diagnostic_logics( factory_config, runtime_logics):
	diagnostic_logics={}
	modules=[f.stem for f in logic_dir.iterdir() if f.suffix==".py" and f.name!="__init__.py"]
	for m in modules:
		module=importlib.import_module(f"decision_maker_package.decision_maker_diagnostic_logics_v1.{m}")
		cls=getattr(module,m)
		diagnostic_logics[m]=cls(factory_config,runtime_logics)
	return diagnostic_logics