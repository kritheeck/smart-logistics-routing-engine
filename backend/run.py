import os
from fastapi import FastAPI
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# CREATE FASTAPI APP (THIS WAS MISSING)
app = FastAPI(
    title="Smart Logistics Routing API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# IMPORT ROUTES
from routes import router
app.include_router(router, prefix="/api")

# START SERVER
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False
    )
