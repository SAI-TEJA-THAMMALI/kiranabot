from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="KiranaBot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "KiranaBot API running"}

@app.get("/ping")
def ping():
    return {"status": "working"}
