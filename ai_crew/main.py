from typing import Union
from fastapi import FastAPI
from datetime import datetime

from src.ai_crew.crew import AiCrew

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/api/v1/legalEntities")
async def read_root():
    return {"Test kiss": "STAR WARS! STAR WARS! STAR WARS!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/v1/runCrew")
async def run_crew():
    inputs = {
        'topic': 'Bio chemistry',
        'current_year': str(datetime.now().year)
    }
    try:
        AiCrew().crew().kickoff(inputs=inputs)
        return {"status": "success", "result": "Crew run successfully"}
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    

