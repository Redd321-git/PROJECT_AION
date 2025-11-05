from fastapi import FastAPI
from . import install_ollama, load_model, force_unload_model, check_if_loaded

app=FastAPI()
	
models={
	"actionset":						#did not specify model name
	"reason":None						#did not specify model name
	"logic":						#did not specify model name
}

@app.post("/generate_actionset")
async def generate_actionset(message: dict):
	if check_if_loaded("actionset") is None:
		load_model("actionset",model["actionset"])
	ollama.generate(
			model=models["actionset"],
			prompt=message
		)
	return

@app.post("/generate_reason")
async def generate_reason(message: dict):
	if check_if_loaded("actionset") is None:
		load_model("actionset",model["actionset"])
	ollama.chat(
			model=models["reason"],
			messages=message
		)
	return

@app.post("/generate_logic")
async def generate_logic(message: dict):
	if check_if_loaded("logic") is None:
		load_model("logic",model["logic"])
	ollama.generate(
			model=models["logic"],
			prompt=message
	)
	return
 
if __name__=="__main__":
	install_ollama()
	
	uvicorn.run("main.app",host=,reload=True)