import threading
from time import sleep
import requests
from pydantic.main import create_model


class Controller():

    def fetch_inputs(cls):
        # TODO alle 0,5s den Reader abfragen

        while True:
            print("fetch_inputs")
            answer = requests.get("http://127.0.0.1:8000/fetch-inputs")
            print(answer)
            sleep(0.5)
            print("waited 0,5 seconds")

            cls.transport(answer)

    def transport(self, reader_data):
        print("transporting data")

        answer = requests.post("http://127.0.0.1:8000/append-to-db", reader_data)
        print(answer)

    def update_view(self):
        db_response = requests.get("http://127.0.0.1:8000/return-db")
        all_data = db_response.content
        all_data_model = self.get_all_data_model_from_dict(all_data)

        requests.post("https://127.0.0.1:8000/update-view", all_data_model)

    def get_all_data_model_from_dict(self, all_data):
        AllDataModel = create_model("AllData", **all_data)
        all_data_model = AllDataModel.parse_obj(all_data)
        return all_data_model

    def trigger_view_updates(self):
        while True:
            sleep(0.5)
            self.update_view()
            print("Requested view update")


if __name__ == '__main__':
    controller = Controller()  # wird umbenannt

    reader_thread = threading.Thread(target=controller.fetch_inputs())
    reader_thread.start()
    output_thread = threading.Thread(target=controller.trigger_view_updates())
    output_thread.start()

