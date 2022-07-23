import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.api_routers.mathcmaking import matchmaking_router

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:63343",
    "http://localhost:3000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matchmaking_router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=7000)
