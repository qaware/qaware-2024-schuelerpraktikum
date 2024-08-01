import os
import requests

import motor
from fastapi import FastAPI
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("data")


@app.get("/return-db", response_description="Returned database dict")
async def returnDB():
    data = await db["data"].find().to_list(1) # TODO: data structure unklar
    latest_data = None
    # db is created in appendToDb if empty
    if len(data) == 0:
        print("Empty db")
        latest_data = {}
    else:
        latest_data = data[-1]

    return JSONResponse(status_code=status.HTTP_200_OK, content=latest_data)


@app.get("/return-db", response_description="Returned database dict")
async def appendToDB(new_raw_data):
    current_db = await returnDB()
    current_sensor_db = current_db[new_raw_data["type"]][new_raw_data["name"]]

    new_sensor_entry = {
        "pressure": new_raw_data["pressure"],
        "temperature": new_raw_data["temperature"],
        "timestamp": new_raw_data["timestamp"]
    }

    current_sensor_db.append(new_sensor_entry)

    await saveDB(current_db)


@app.post("/create", response_description="Initial")
async def createDB():
    initial_data = {"data": {}}
    json = jsonable_encoder(initial_data)
    await db["data"].insert_one(json)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")



if __name__ == '__main__':
    # resp1 = requests.post("http://127.0.0.1:8000/create")
    resp1 = requests.get("http://127.0.0.1:8000/return-db")
    print(resp1.status_code, resp1.content)
