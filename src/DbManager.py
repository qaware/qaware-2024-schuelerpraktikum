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


async def get_latest_db_contents():
    db_contents = await db["data"].find().to_list(1)  # [{'_id': ObjectId('66ab3cfc7e7a9c72fbac78c8'), 'data': {}}]

    # db is created in appendToDb if empty
    if len(db_contents) == 0:
        print("Empty db")
        latest_data = {}
    else:
        latest_data = db_contents[-1]

    return latest_data


@app.get("/return-db", response_description="Returned database dict")
async def return_db():
    latest_data = await get_db()

    return JSONResponse(status_code=status.HTTP_200_OK, content=latest_data)


async def get_db():
    latest_content = await get_latest_db_contents()
    latest_data = latest_content["data"]
    return latest_data


# @app.get("/get-id", response_description="Returned database dict id")
async def get_latest_db_id():
    latest_content = await get_latest_db_contents()
    latest_id = latest_content["_id"]

    # return JSONResponse(status_code=status.HTTP_200_OK, content=latest_id_str)
    return latest_id


@app.post("/save", response_description="Save db")
async def save_db(new_data):
    # print("save db executed")
    latest_id = await get_latest_db_id()
    print(latest_id)
    print("latest id", latest_id)
    await db["data"].update_one({"_id": latest_id}, {"$set": jsonable_encoder({"data": new_data})})
    print("Updated")
    return JSONResponse(status_code=status.HTTP_200_OK, content="")


def get_current_sensor_db(current_db, sensor_type, sensor_name):
    if sensor_type not in current_db:
        current_db[sensor_type] = {}

    if sensor_name not in current_db:
        current_db[sensor_type][sensor_name] = []

    current_sensor_db = current_db[sensor_type][sensor_name]

    return current_sensor_db


@app.post("/append-to-db", response_description="Returned database dict")
async def append_to_db():
    new_raw_data = {
        "name": "sa",
        "type": "dad",
        "pressure": 12,
        "temperature": 231,
        "timestamp": 10001
    }

    print("Appending")
    current_db = await get_db()
    print("Mapping", current_db)

    current_sensor_db = get_current_sensor_db(current_db, new_raw_data["type"], new_raw_data["name"])

    new_sensor_entry = {
        "pressure": new_raw_data["pressure"],
        "temperature": new_raw_data["temperature"],
        "timestamp": new_raw_data["timestamp"]
    }

    current_sensor_db.append(new_sensor_entry)

    await save_db(current_db)


@app.post("/create", response_description="Initial")
async def create_db():
    initial_data = {"data": {}}
    json = jsonable_encoder(initial_data)
    await db["data"].insert_one(json)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")


if __name__ == '__main__':
    resp1 = requests.post("http://127.0.0.1:8000/append-to-db")
    resp1 = requests.get("http://127.0.0.1:8000/return-db")
    print(resp1.status_code, resp1.content)
