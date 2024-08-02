import datetime
import os
from typing import List

import datetime as dt

from bson.json_util import dumps

from cryptography.fernet import Fernet

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

key = "t1Zerro4GwUqPMWbpVBsfnhF2Zkl3FRfXyLzFj33gQk="
cy = Fernet(key)


# Groundstation
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
    await database_backup()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


# User
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


@app.get("/data/getTimeType/{time}/{data_type}",
         response_description="Return all data of the selected type, after the time given",
         response_model=List[SensorData])
async def get_by_time_type(time: str, data_type: str):
    found_data = await find_data({"data_type": data_type})
    return JSONResponse(content=filter_by_time(time, found_data))


@app.get("/data/getTimeName/{time}/{name}",
         response_description="Return all data of the selected name, after the time given",
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


@app.get("/data/allTypes/", response_model=List[str], response_description="Get all unique types")
async def all_types():
    found_types = await db["data"].distinct("data_type")
    return JSONResponse(content=found_types)


@app.get("/data/allNames/", response_model=List[str], response_description="Get all unique names")
async def all_names():
    found_types = await db["data"].distinct("name")
    return JSONResponse(content=found_types)


@app.get("/data/typesByName/{name}", response_model=List[str],
         response_description="Get all unique types, for the given name")
async def types_by_name(name: str):
    found_types = await db["data"].distinct("data_type", filter={"name": name})
    return JSONResponse(content=found_types)


@app.get("/data/namesByType/{data_type}", response_model=List[str],
         response_description="Get all unique names, for the given type")
async def names_by_type(data_type: str):
    found_types = await db["data"].distinct("name", filter={"data_type": data_type})
    return JSONResponse(content=found_types)


@app.get("/dump/", response_model=str, response_description="return the latest dump")
async def dump():
    arr = os.listdir("dumps/")
    dates = []
    for i in arr:
        dates.append(datetime.datetime.fromisoformat(i[5:-10]))
    dump = open(f"./dumps/dump_{datetime.datetime.isoformat(sorted(dates, reverse=True)[0])}.json.encr").read()
    return JSONResponse(content=dump)


def filter_by_time(time: str, data: List):
    return_data = []
    timestamp = int(time)
    for obj in data:
        if int(obj["time"]) > timestamp:
            return_data.append(obj)
    return return_data


async def find_data(args: dict[str, str]):
    return await db["data"].find(args).to_list(1000)


async def database_backup2():
    print("saving database")
    data = dumps(await db["data"].find().to_list(1000))
    savefile = open(f"./dumps/dump_{dt.datetime.isoformat(dt.datetime.now())}.json", "w")
    savefile.write(data)
    savefile.close()


async def database_backup():
    all_sensors: [dict[str, str]] = []
    found_names = await db["data"].distinct("name")
    for name in found_names:
        found_types = await db["data"].distinct("data_type", filter={"name": name})
        for data_type in found_types:
            all_sensors.append({"name": name, "data_type": data_type})

    data_to_save = []
    for sensor_description in all_sensors:
        data_found= await find_data(sensor_description)
        data_to_save.append(sorted(data_found, key=lambda x: x["time"], reverse=True)[0])

    data = dumps(data_to_save)
    encr_string = cy.encrypt(data.encode())
    savefile = open(f"./dumps/dump_{dt.datetime.isoformat(dt.datetime.now())}.json.encr", "w")
    savefile.write(encr_string.decode())
    savefile.close()


os.makedirs("./dumps/", exist_ok=True)
