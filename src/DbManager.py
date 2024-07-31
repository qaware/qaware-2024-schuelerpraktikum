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


@app.get("/return-db", response_description="Returned database dict")
async def returnDB():
    data = await db["data"].find().to_list(1000)
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


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

    await save_db(current_db)

@app.put("/save", response_description="Test save")
async def save_db():
    test = ["test"]
    await db["data"].update(test)
    return JSONResponse(status_code=status.HTTP_200_OK)



if __name__ == '__main__':
    resp1 = requests.post("http://127.0.0.1:8000/save")
    print(resp1)
    resp = requests.get("http://127.0.0.1:8000/returndb")
    print(resp.status_code, resp.content)
