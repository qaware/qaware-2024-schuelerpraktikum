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
async def returnDB():
    latest_content = await get_latest_db_contents()
    latest_data = latest_content["data"]

    return JSONResponse(status_code=status.HTTP_200_OK, content=latest_data)


@app.get("/get-id", response_description="Returned database dict id")
async def get_latest_db_id():
    latest_content = await get_latest_db_contents()
    latest_id = latest_content["_id"]
    latest_id_str = str(latest_id)
    # print("latest id:", latest_id, type(latest_id), latest_id_str)

    return JSONResponse(status_code=status.HTTP_200_OK, content=latest_id_str)


@app.post("/save", response_description="Initial")
async def saveDB():
    print("test")
    latest_id_request = requests.post("http://127.0.0.1:8000/get-id")
    # latest_id = await get_latest_db_id()
    latest_id = latest_id_request.content
    print("latest id", latest_id)
    # await db["data"].update_data({"_id": latest_id}, {"data": "t22"})


@app.get("/append-to-db", response_description="Returned database dict")
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
    resp1 = requests.post("http://127.0.0.1:8000/save")
    resp1 = requests.get("http://127.0.0.1:8000/return-db")
    print(resp1.status_code, resp1.content)
