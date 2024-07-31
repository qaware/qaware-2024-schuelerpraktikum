import json
import os
from typing import List

import motor
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse

from models import SensorData

app = FastAPI()
os.environ["MONGODB_URL"] = "mongodb://root:password@localhost:27017/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.get_database("data")


# Bodenstation
@app.get("/data/doesExist/{data_type}/{name}/{time}",
         response_description="Check if Data already exists, returns true if data exists. "
                              "Checks if an entry for the exact sensor at the same time already exists",
         response_model=bool)
async def data_does_exist(data_type: str, name: str, time: str):
    found_data = await db["data"].find_one({"data_type": data_type, "name": name, "time": int(time)})
    return JSONResponse(status_code=200, content=found_data is not None)


@app.post("/data/addData/", response_description="Add data, returns data added", response_model=SensorData)
async def add_sensor_data(data: SensorData):
    new_data = await db["data"].insert_one(jsonable_encoder(data))
    created_data = await db["data"].find_one({"_id": new_data.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


# Nutzer
@app.get("/data/getType/{data_type}", response_description="Return all data of the selected type",
         response_model=List[SensorData])
async def get_by_type(data_type: str):
    found_data = await find_data({"data_type": data_type})
    return JSONResponse(content=found_data)


@app.get("/data/getName/{name}", response_description="Return all data of the selected name",
         response_model=List[SensorData])
async def get_by_name(name: str):
    found_data = await find_data({"name": name})
    return JSONResponse(content=found_data)


@app.get("/data/getTypeName/{data_type}/{name}", response_description="Return all data of the selected type and name",
         response_model=List[SensorData])
async def get_by_type_name(data_type: str, name: str):
    found_data = await find_data({"data_type": data_type, "name": name})
    return JSONResponse(content=found_data)


@app.get("/data/getTimeType/{time}/{data_type}", response_description="Return all data of the selected type, after the time given",
         response_model=List[SensorData])
async def get_by_time_type(time: str, data_type: str):
    found_data = await find_data({"data_type": data_type})
    return JSONResponse(content=filter_by_time(time, found_data))


@app.get("/data/getTimeName/{time}/{name}", response_description="Return all data of the selected name, after the time given",
         response_model=List[SensorData])
async def get_by_time_name(time: str, name: str):
    found_data = await find_data({"name": name})
    return JSONResponse(content=filter_by_time(time, found_data))


@app.get("/data/getTimeTypeName/{time}/{data_type}/{name}",
         response_description="Return all data of the selected type and name, after the time given",
         response_model=List[SensorData])
async def get_by_time_type_name(time: str, data_type: str, name: str):
    found_data = await find_data({"data_type": data_type, "name": name})
    return JSONResponse(content=filter_by_time(time, found_data))


def filter_by_time(time: str, data: List):
    return_data = []
    timestamp = int(time)
    for obj in data:
        if int(obj["time"]) > timestamp:
            return_data.append(obj)
    return return_data


async def find_data(args: dict[str, str]):
    return await db["data"].find(args).to_list(1000)
