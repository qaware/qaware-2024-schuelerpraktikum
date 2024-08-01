import json
from os import listdir
from typing import List
from starlette.responses import JSONResponse
from starlette import status
from fastapi import FastAPI

app = FastAPI()


@app.get("/fetch-inputs/", response_description="Fetch raw data", response_model=List[dict])
async def fetch_inputs():
    dict_list = read_files()
    return JSONResponse(status_code=status.HTTP_200_OK, content=dict_list)


PATH = '../data/'
newest_file = ''


def read_files():
    global newest_file
    save = open('../saves/last_saved_file.txt', 'r')
    newest_file = save.read()
    save.close()

    fileNameList = [fileName for fileName in listdir(PATH) if fileName.startswith("TM") and fileName.endswith(".json")]
    currentNewestFile = newest_file
    dict_list = []
    for fileName in fileNameList:
        if fileName > newest_file:
            data = open(PATH + fileName, "r")
            timestamp = fileName[3:-5]
            data_dict = json.load(data)
            data_dict["timestamp"] = timestamp
            dict_list.append(data_dict)
            if fileName > currentNewestFile:
                currentNewestFile = fileName
    newest_file=currentNewestFile
    save = open('../saves/last_saved_file.txt', 'w')
    save.write(newest_file)
    save.close()
    return dict_list
