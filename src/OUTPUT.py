# TODO Warnung bei kritischen Werten

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette import status

app = FastAPI()



@app.post("/update-view/", response_description="Recieve data to update view")
async def create_data(data: dict):
    update_table(data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)



def update_table(data: dict):

    item={}
    data={
        "thruster": {
            "thruster_3.b": [
                {
                    "pressure": 0.222,
                    "temperature": 0.22,
                    "timestamp": 12887729
                },
                {
                    "pressure": 0.2322,
                    "temperature": 0.32,
                    "timestamp": 12887398
                }
            ],
            "thruster_3.a": [
                {
                    "pressure": 0.2322,
                    "temperature": 0.32,
                    "timestamp": 12887398
                }
            ]
        },
        "gas_valve": {
            "gas_valve1":[
                {
                    "pressure": 0.322,
                    "temperature": 0.33,
                    "timestamp": 13333333
                },
                {
                    "pressure": 0.666,
                    "temperature": 0.66,
                    "timestamp": 16666668
                }
            ]
        }
    }
    fig, ax = plt.subplots()
    rowLabels=["Sensor Type", "Sensor Name","Temperature","Pressure"]

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)
    # TODO: erstelle tabelle

    df2=pd.DataFrame()
    item_number=0
    for sensor_type in data.keys():
        item["type"] = sensor_type
        for name in data[sensor_type].keys():
            item["name"] = name
            data_list = data[sensor_type][name]
            item["pressure"] = data_list[-1]["pressure"]
            item["temperature"]=data_list[-1]["temperature"]
            item["timestamp"]=data_list[-1]["timestamp"]
            df=pd.DataFrame({'type': item["type"],
                             'name': item["name"],
                             'pressure': item["pressure"],
                             'temperature':item["temperature"],
                             },
                            index=[item["timestamp"]])
            df2 = df2 + df
            print(df)
            item_number=item_number+1

            # TODO: schreibe neues item in tabelle rein

    df2=df2.T

    print(df2.values)
    table = ax.table(cellText=df2,
                     rowLabels=rowLabels,
                     cellLoc='center',
                     loc='center')
    i=0
    while i<4:
        cell=table[(i,-1)]
        i=i+1
        cell.get_text().set_color('midnightblue')
        cell.get_text().set_fontsize(20)
        cell.get_text().set_fontweight("bold")
        cell.set_facecolor("azure")



    table.scale(xscale=1, yscale=2)

    plt.subplots_adjust(left=0.5, top=0.8)

    plt.show()

data={}
update_table(data)