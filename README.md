# QAware Schülerpraktikum 2024

Repository to store code, which is used at the Schülerpraktikum 2024 at QAware.

## Installation

0.) Optionally create a virtual environment for your python packages of this project:

```
python3 -m venv venv
source venv/bin/activate
```

1.) Install all dependencies:

```
pip install -r requirements.txt
```

2.) Start the database:

```
docker compose up -d
```

3.) Start the uvicorn backend:

```
uvicorn BeispielVerwaltung:app --reload
```

The reload command is used to be able to update the code and start the application automatically.

## Usage

After the installation the API can be called via curl or the browser to serve the user with data or as data storage.

For example: \
http://127.0.0.1:8000/hello_world 

A more generalized overview of existing APIs can be retrieved in a Swagger UI under:
http://127.0.0.1:8000/docs

## Helpful Links

- [AsyncIOMotorClient – Connection to MongoDB](https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_client.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Git Documentation](https://git-scm.com/docs)

## Maintainer

R. Kalleicher, <robin.kalleicher@qaware.de>
T. Schneider, <thea.schneider@qaware.de>     
N. Feifel, <nina.feifel@qaware.de>

## Initial Code and Idea

R. Kalleicher, <robin.kalleicher@qaware.de>     
C. Thelen, <christoph.thelen@qaware.de>