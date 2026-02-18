from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.insight_routes import router as insight_router

app = FastAPI(title="Live Like a Local API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insight_router, prefix="")

@app.get("/health")
def health():
    return {"status": "ok"}
