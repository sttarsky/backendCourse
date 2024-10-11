import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as auth_router
from src.api.hotels import router as hotel_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(hotel_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
