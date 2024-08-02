from time import sleep
import requests


class Controller():

    def fetch_inputs_and_transport(self):
        # alle 0,5s den Reader abfragen

        while True:
            print("fetching inputs")
            answer = requests.get("http://127.0.0.1:8001/fetch-inputs")
            print(answer)
            print(answer.content)
            self.transport(answer)
            sleep(0.5)
            print("waited 0.5 seconds")

    def transport(self, reader_data):
        print("transporting data")
        for sensor_input in reader_data:
            print(requests.post("http://127.0.0.1:8002/append-to-db", sensor_input))


if __name__ == '__main__':
    controller = Controller() # wird umbenannt
    controller.fetch_inputs_and_transport() # ein Befehl
