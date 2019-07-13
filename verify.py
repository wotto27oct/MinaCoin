import ecdsa
import filelock
import hashlib
import json

with filelock.FileLock("trans.lock", timeout=10):
    with open("trans.txt", "r") as file:
        tx_list = json.load(file)

for tx in tx_list:
    print("in hex:", tx["in"])
    print("out hex:", tx["out"])
    print("sig hex:", tx["sig"])

# from hex to binary
    tx_in = bytes.fromhex(tx["in"])
    tx_out = bytes.fromhex(tx["out"])
    tx_sig = bytes.fromhex(tx["sig"])

    sha = hashlib.sha256()
    sha.update(tx_in)
    sha.update(tx_out)
    hash=sha.digest()

    print("hash len:", len(hash))
    print("hash hex:", hash.hex())

    key = ecdsa.VerifyingKey.from_string(tx_in, curve=ecdsa.SECP256k1)
    print("veryfy:", key.verify(tx_sig, hash))

    print()
