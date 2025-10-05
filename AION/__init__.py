from pathlib import Path
import importlib.util
import json

AION_Dependencies=Path(__file__).resolve().parents[1]/"AION_dependencies"
AION_Runtime=Path(__file__).resolve().parents[1]/"AION_rutime"

def load_factory_config():
	with open(AION_Dependencies/"factory_policy_config.json",'r') as f:
		factory_config=json.load(f)
	return factory_config

def load_runtime_logics():
	modules=[f.stem for f in AION_Runtime.iterdir() if f.suffix==".py" and f.name!="__init__.py"]
	runtime_logics={}
	for m in modules:
		module=importlib.import_module(f"AION_Runtime.{m}")
		cls=getattr(module,m)
		runtime_logics[m]=cls()
	return runtime_logics