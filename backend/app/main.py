from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from .api.routes import router
from .middleware.error_handler import setup_error_handlers

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "Smart Logistics Routing Engine"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="Production-ready logistics routing system using Dijkstra's algorithm",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
setup_error_handlers(app)
app.include_router(router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Smart Logistics Routing Engine API", "version": "1.0.0", "documentation": "/api/docs"}
