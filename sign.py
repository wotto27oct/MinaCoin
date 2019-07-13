import base58
import ecdsa
import filelock
import hashlib
import json 
import sys

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "in-private in-public out_public")
    exit()

# convert from base58 to binary
tx_key = base58.b58decode(sys.argv[1])
tx_in = base58.b58decode(sys.argv[2])
tx_out = base58.b58decode(sys.argv[3])

print("key hex:", tx_key.hex())
print("in hex:", tx_in.hex())
print("out hex:", tx_out.hex())

# create transaction hash
sha = hashlib.sha256()
sha.update(tx_in)
sha.update(tx_out)
hash = sha.digest()

print("hash len:", len(hash))
print("hash hex:", hash.hex())

# create sign for transaction hash
key = ecdsa.SigningKey.from_string(tx_key, curve=ecdsa.SECP256k1)
sig = key.sign(hash)

print("sig len:", len(sig))
print("sig hex:", sig.hex())

with filelock.FileLock("trans.lock", timeout=10):
    try:
        with open("trans.txt", "r") as file:
            tx_list = json.load(file)
    except:
        tx_list = []

    tx_list.append({
        "in": tx_in.hex(),
        "out": tx_out.hex(),
        "sig": sig.hex()
        })

    with open("trans.txt", "w") as file:
        json.dump(tx_list, file, indent=2)
