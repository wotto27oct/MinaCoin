import base58
import ecdsa
import filelock
import json

# generate private_key and public_key by using ecdsa (curve: SECP256k1)
private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key()

# convert to string
private_key = private_key.to_string()
public_key = public_key.to_string()

print("private key len:", len(private_key))
# convert from string to hexadecimel
print("private key hex:", private_key.hex())

print("public key len:", len(public_key))
print("public key hex:", public_key.hex())

# convert to base58
private_b58 = base58.b58encode(private_key).decode('ascii')
public_b58 = base58.b58encode(public_key).decode('ascii')

print("private key base58:", private_b58)
print("public key base58:", public_b58)

with filelock.FileLock("key.lock", timeout=10):
    try:
        with open("key.txt", "r") as file:
            key_list = json.load(file)
    except:
        key_list = []

    key_list.append({
        'private': private_b58,
        'public': public_b58
        })
        
    with open("key.txt", "w") as file:
        json.dump(key_list, file, indent=2)

