import os
from cryptography.fernet import Fernet
from bson.json_util import loads
import json

key = "t1Zerro4GwUqPMWbpVBsfnhF2Zkl3FRfXyLzFj33gQk="
cy = Fernet(key)

arr = os.listdir("dumps/")

for x in arr:
    enc_str = open(f"dumps/{x}", "r").read()
    print("\n\n\n")
    print(x)
    print(json.dumps(loads(cy.decrypt(enc_str).decode()), indent=2, ))
