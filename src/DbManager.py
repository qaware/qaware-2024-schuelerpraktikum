import os
import requests

import motor
from fastapi import FastAPI
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("data")


@app.get("/returndb", response_description="Returned database dict")
def returndb():
    response = "Hello World"
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


if __name__ == '__main__':
    resp = requests.get("http://127.0.0.1:8000/returndb")
    print(resp.status_code, resp.content)
