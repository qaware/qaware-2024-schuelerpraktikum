import os

import motor
from fastapi import FastAPI
from motor import motor_asyncio
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.ModelHandling import ModelMapper
from src.ModelHandling import SensorDataModel

app = FastAPI()
mapper = ModelMapper()
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
    if latest_content == {}:
        return {}

    latest_data = latest_content["data"]
    return latest_data


async def get_latest_db_id():
    latest_content = await get_latest_db_contents()
    latest_id = latest_content["_id"]

    return latest_id


@app.post("/save", response_description="Save db")
async def save(new_data):
    print("save db executed")
    await save_db(new_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content="")


async def save_db(new_data):
    latest_id = await get_latest_db_id()
    await db["data"].update_one({"_id": latest_id}, {"$set": jsonable_encoder({"data": new_data})})


def get_current_sensor_db(current_db, sensor_type, sensor_name):
    if sensor_type not in current_db:
        current_db[sensor_type] = {}
        print("Type doesn't exist, creating", sensor_type)

    if sensor_name not in current_db[sensor_type]:
        current_db[sensor_type][sensor_name] = []
        print("Sensor doesn't exist, creating", sensor_name)

    current_sensor_db = current_db[sensor_type][sensor_name]

    return current_sensor_db


async def db_is_empty():
    db = await get_db()
    return db == {}


@app.post("/append-to-db", response_description="Returned database dict")
async def append_to_db(new_raw_data_model: SensorDataModel):
    if await db_is_empty():
        print("Creating database")
        await create_db()
    else:
        print(" DB not empty")

    print("Appending", new_raw_data_model)
    new_raw_data = mapper.model_to_dict(new_raw_data_model)

    current_db = await get_db()
    print("Mapping", current_db)

    current_sensor_db = get_current_sensor_db(current_db, new_raw_data["type"], new_raw_data["name"])
    print(current_sensor_db)
    new_sensor_entry = {
        "pressure": new_raw_data["pressure"],
        "temperature": new_raw_data["temperature"],
        "timestamp": new_raw_data["timestamp"]
    }
    current_sensor_db.append(new_sensor_entry)

    print(current_db)
    await save(current_db)


@app.post("/create", response_description="Initial")
async def create_db():
    print("Creating db")
    initial_data = {"data": {}}
    json = jsonable_encoder(initial_data)
    await db["data"].insert_one(json)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="")

# if __name__ == '__main__':
# Example input
# data = {
#     "name": "AA",
#     "type": "AA2224",
#     "pressure": 12.5,
#     "temperature": 0,
#     "timestamp": "10001236"
# }
#
# data = mapper.dict_to_model(data)

# resp1 = requests.post("http://127.0.0.1:8000/append-to-db", data.json())
# resp1 = requests.get("http://127.0.0.1:8000/return-db")

# print(resp1.status_code, resp1.content)
