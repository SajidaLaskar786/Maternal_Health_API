from fastapi import FastAPI
from mock_model import call_maternal_health_model
app = FastAPI()

@app.get("/mht/")
def read_root():
    return {"message": "Hello, FastAPI is running!"}

@app.post("/mht/")
def submit_health_status(params: dict):
    ht = float(params['height']) + 2
    wt = float(params['weight']) + 30
    det = params['diet'] 
    health_status = call_maternal_health_model(height=ht, weight=wt, diet=det)
    return {
        "health status": health_status
    }
