# TODO Warnung bei kritischen Werten

import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette import status

PATH = "./images/"
FILENAME = "Output.png"

app = FastAPI()



@app.post("/update-view/", response_description="Recieve data to update view")
async def create_data(data: dict):
    update_table(data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=None)



def update_table(data: dict):

    # Transformiere Daten
    table_data = []
    for sensor_type in data.keys():
        for name in data[sensor_type].keys():
            data_list = data[sensor_type][name]
            item = data_list[-1]

            row = [
                sensor_type,
                name,
                item["pressure"],
                item["temperature"],
            ]
            table_data.append(row)

    # Daten in einen DataFrame umwandeln und transponieren
    df = pd.DataFrame(table_data, columns=["Sensor Type", "Sensor Name", "Pressure", "Temperature"])
    df = df.T

    # Erstelle Tabellen Plot
    fig, ax = plt.subplots()
    rowLabels=["Sensor Type", "Sensor Name","Temperature","Pressure"]

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    table = ax.table(cellText=df.values,
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

    # Speichern der Tabelle in eine Datei
    plt.savefig(PATH + FILENAME, bbox_inches='tight', dpi=600)

# Zum testen
# data={
#     "thruster": {
#         "thruster_3.b": [
#             {
#                 "pressure": 0.222,
#                 "temperature": 0.22,
#                 "timestamp": 12887729
#             },
#             {
#                 "pressure": 0.2322,
#                 "temperature": 0.32,
#                 "timestamp": 12887398
#             }
#         ],
#         "thruster_3.a": [
#             {
#                 "pressure": 0.2322,
#                 "temperature": 0.32,
#                 "timestamp": 12887398
#             }
#         ]
#     },
#     "gas_valve": {
#         "gas_valve1":[
#             {
#                 "pressure": 0.322,
#                 "temperature": 0.33,
#                 "timestamp": 13333333
#             },
#             {
#                 "pressure": 0.666,
#                 "temperature": 0.66,
#                 "timestamp": 16666668
#             }
#         ]
#     }
# }
# update_table(data)