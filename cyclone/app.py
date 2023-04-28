from fastapi import FastAPI
from .utilities.env import load_env

app = FastAPI()

load_env()
