from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import redis

my_redis = redis.Redis(
    host="redis", password="pseudolab", port=6379, decode_responses=True
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return my_redis.get("current_state") if my_redis.get("current_state") else ""
