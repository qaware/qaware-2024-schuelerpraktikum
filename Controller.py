from time import sleep
import requests


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



if __name__ == '__main__':
    controller = Controller() # wird umbenannt
    controller.fetch_inputs() # ein Befehl



