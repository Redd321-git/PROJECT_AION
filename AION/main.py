from fastapi import FastAPI
from aion import AION
from typing import Optional
from env_interfaces import Environment
from models import AgentState
from fastapi.templating import Jinja2Templates

app=FastAPI()

aion: Optional[AION] = None
ENV_connection: Optional[Environment] = None


AION_ENABLED= AgentState.Stopped



@app.post("/register",response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
	existing_user =get_user_by_email(db,user.email)
	if existing_user:
		raise HTTPException(status_code=400,detail="Email already registered")
	user=create_user(db, user)
	create_user_stream(user.id)
	return user

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
	user=get_user_by_username(db,form_data.username)
	
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	
	access_token = create_access_token(
		data={"sub":user.email}, expires_delta=timedelta(minutes=access_token_expire_minutes)
	)
	return {"access_token": access_token, "token_type": "bearer","message":"login successfull"}

@app.get("/me",response_model=UserResponse)
async def read_me(current_user= Depends(get_current_user)):
	return current_user


@app.post("/connect_env")
async def connect_env(env : Environment):
	global ENV_connection
	if ENV_connection :
		return {"status":"already connected"}
	ENV_connection= env
	return {"status":"environment connected"}

@app.post("/disconnect_env")
async def disconnect_env():
	global ENV_connection
	if not ENV_connection :
		return {"status":"already disconnected"}
	ENV_connection.disconnect()
	ENV_connection=None
	return {"status":"environment disconnected"}

@app.post("/aion_start")
async def start_aion():
	global AION_ENABLED , ENV_connection, AION_ENABLED, aion
	if AION_ENABLED == AgentState.Running:
		return {"status": "agent already running"}
	if not ENV_connection:
		return {"status":"environment not connected"}
	aion=AION(ENV_connection)
	aion.start()
	AION_ENABLED= AgentState.Running
	return {"status":"AION up and running"}
	
	
@app.post("/aion_stop")
async def stop_aion():
	global AION_ENABLED , ENV_connection, AION_ENABLED, aion
	if AION_ENABLED == AgentState.Stopped:
		return {"status": "agent already stopped"}
	if not ENV_connection:
		return {"status":"environment not connected"}
	aion.stop()
	AION_ENABLED= AgentState.Stopped
	return {"status":"AION stopped"}
	
@app.get("/AION_state")
async def get_state():
	return {"status":aion.aion_state}

if __name__=="__main__":
	import uvicorn
	uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)