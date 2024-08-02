import os
from cryptography.fernet import Fernet
from bson.json_util import loads
import json
import pathlib

key = "t1Zerro4GwUqPMWbpVBsfnhF2Zkl3FRfXyLzFj33gQk="
cy = Fernet(key)

arr = os.listdir("dumps/")

os.makedirs("decodedDumps/", exist_ok=True)

for x in arr:
    enc_str = open(f"dumps/{x}", "r").read()
    pathlib.Path(f"decodedDumps/{x}"[0:-5]).unlink(missing_ok=True)
    saveFile = open(f"./decodedDumps/{x}"[0:-5], "w")
    print("\n\n\n")
    print(x)
    decrypted_str= json.dumps(loads(cy.decrypt(enc_str).decode()), indent=2, )
    saveFile.write(decrypted_str)
    saveFile.close()
    print(decrypted_str)

