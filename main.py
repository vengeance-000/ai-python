from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import router

app = FastAPI(
    title="vengeance-ai-python",
    description="A modular backend for AI Agents written in python",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "LLM Backend Utilities is running."}
