from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.insight_routes import router as insight_router
import os

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

if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
