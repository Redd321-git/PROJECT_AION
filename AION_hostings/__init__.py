import ollama
import subprocess
import time
import asyncio
import requests 

def install_ollama():
	try:
		subprocess.run(["ollama","--version"],check=True)
		print("ollama already installed")
	except FileNotFoundError:
		print("Install ollama")
		
	except subprocess.CalledProcessError:
		print("ollama not found")

loaded_models={
	"actionset":None,
	"logic":None
}
locks={
	"logic":asyncio.Lock(),
	"actionset":asyncio.Lock()
}
last_access={
	"logic":None
}

UNLOAD_TIMEOUT=								# need to descide 
async def load_model(task_type:str,model_name:str):
	async with locks[task_type]:
		if loaded_models[task_type] is None:
			try:
				result=subprocess.run(["ollama","pull",model_name],capture_output=True,text=True,check=True)
				loaded_models[task_type]=model_name		
				print(f"model loaded {model_name}")
				print(result)
				if task_type=="logic":
					last_access[task_type]=time.time()
			except subprocess.CalledProcessError as e:
				print("load failed")
				print(e)
		
	return loaded_models[task_type]

async def check_if_loaded(task_type:str):
	if loaded_models[task_type]:
		return True
	return False

async def force_unload_model(model_name:str):
	while True:
		await asyncio.sleep()					# need to specify sleep time
		async with locks["logic"]:
			if loaded_models["logic"]:
				idle_time=time.time()-last_access("logic",0)
				if idle_time>UNLOAD_TIMEOUT:
					try:
						requests.post("http://loaclhost:11434/api/stop",json={"model":model_name})
						loaded_models["logic"]=None
						print(f"model unloaded {model_name}")
					except Exception as e:
						print(e)