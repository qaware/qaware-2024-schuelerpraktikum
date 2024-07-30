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

# TODO: Welche Daten müssen zur Verfügung gestellt werden?
# TODO: Wie verhindern wir, dass beschädigte Daten in das System gelangen?
# TODO: Wie melden wir Nutzern zurück, dass keine Sensordaten vorhanden sind?
# TODO: Wie melden wir Nutzern, dass bereits ein entsprechendes Datenset existiert?
# TODO: Was gehört zur Verwaltung der Daten noch?
# TODO: Benötigen wir noch andere Schnittstellen für unsere Nutzer?

"""
@app.get("/hello_world", response_description="Hello World")
def hello_world():
    response = "Hello World"
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@app.post("/data/", response_description="Create Data", response_model=Sensor_data)
async def create_data(data: Sensor_data):
    new_data = await db["data"].insert_one(jsonable_encoder(data))
    created_data = await db["data"].find_one({"_id": new_data.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


@app.get("/data/", response_description="List All Data", response_model=List[Sensor_data])
async def list_data():
    data = await db["data"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.get("/data/{id}", response_description="Read Data", response_model=Sensor_data)
async def read_data(id: str):
    data = await db["data"].find_one({"_id": id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


@app.put("/data/{id}", response_description="Update Data", response_model=Sensor_data)
async def update_data(id: str, update: UpdateDataModel):
    await db["data"].update_one({"_id": id}, {"$set": jsonable_encoder(update)})
    updated_data = await db["data"].find_one({"_id": id})

    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_data)


@app.delete("/data/{id}", response_description="Delete Data")
async def delete_data(id: str):
    await db["data"].delete_one({"_id": id})
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
"""


# Bodenstation
@app.get("/data/doesExist/{data_type}/{name}/{time}",
         response_description="Check if Data already exists, returns true if data exists",
         response_model=bool)
async def data_does_exist(data_type: str, name: str, time: str):
    found_data = await db["data"].find_one({"data_type": data_type, "name": name, "time": int(time)})
    return found_data is not None


@app.post("/data/addData/", response_description="Add data, returns data added", response_model=SensorData)
async def add_sensor_data(data: SensorData):
    new_data = await db["data"].insert_one(jsonable_encoder(data))
    created_data = await db["data"].find_one({"_id": new_data.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_data)


# Nutzer
@app.get("/data/getType/{data_type}", response_description="Return all data of the selected type",
         response_model=List[SensorData])
async def get_by_type(data_type: str):
    found_data = await db["data"].find({"data_type": data_type}).to_list(1000)
    return JSONResponse(content=found_data)


@app.get("/data/getName/{name}", response_description="Return all data of the selected name",
         response_model=List[SensorData])
async def get_by_type(name: str):
    found_data = await db["data"].find({"name": name}).to_list(1000)
    return JSONResponse(content=found_data)


@app.get("/data/getTypeName/{data_type}/{name}", response_description="Return all data of the selected type and name",
         response_model=List[SensorData])
async def get_by_type(data_type: str, name: str):
    found_data = await db["data"].find({"data_type": data_type, "name": name}).to_list(1000)
    return JSONResponse(content=found_data)


@app.get("/data/getTimeType/{time}/{data_type}", response_description="Return all data of the selected type",
         response_model=List[SensorData])
async def get_by_type(time:str, data_type: str):
    found_data = await db["data"].find({"data_type": data_type}).to_list(1000)
    return JSONResponse(content=filter_by_time(time, found_data))


@app.get("/data/getTimeName/{time}/{name}", response_description="Return all data of the selected name",
         response_model=List[SensorData])
async def get_by_type(time:str, name: str):
    found_data = await db["data"].find({"name": name}).to_list(1000)
    return JSONResponse(content=filter_by_time(time, found_data))


@app.get("/data/getTimeTypeName/{time}/{data_type}/{name}", response_description="Return all data of the selected type and name",
         response_model=List[SensorData])
async def get_by_type(time: str, data_type: str, name: str):
    found_data = await db["data"].find({"data_type": data_type, "name": name}).to_list(1000)
    return JSONResponse(content=filter_by_time(time, found_data))


def filter_by_time(time: str, data):
    return_data = []
    timestamp = int(time)
    for obj in data:
        if int(obj["time"]) > timestamp:
            return_data.append(obj)
    return return_data
