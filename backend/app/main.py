from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import setup_logging
from app.core.config import settings
from app.api.main import api_router
from app.websocket.main import ws_router


setup_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.include_router(api_router)
app.include_router(ws_router)


@app.get("/")
def read_root():
    return {"Welcome": "This is the root endpoint of the API PIT Web Service."}
