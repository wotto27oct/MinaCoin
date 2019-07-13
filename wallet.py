import base58
import filelock
import json

with filelock.FileLock("key.lock", timeout=10):
    try:
        with open("key.txt", "r") as file:
            key_list = json.load(file)
    except:
        key_list = []

with filelock.FileLock("block.lock", timeout=10):
    try:
        with open("block.txt", "r") as file:
            block_list = json.load(file)
    except:
        block_list = []

old_in = []
old_out = []
for block in block_list:
    for tx in block["tx"]:
        old_in.append(tx["in"])
        old_out.append(tx["out"])

unspent = []
unused = []
for key in key_list:
    key_hex = base58.b58decode(key["public"]).hex()
    if key_hex not in old_in:
        if key_hex in old_out:
            unspent.append(key)
        else:
            unused.append(key)

print(len(unspent), "unspent keys(coins):")
for key in unspent:
    print("private:", key["private"])
    print("public:", key["public"])

print()

print(len(unused), "unused keys:")
for key in unused:
    print("private:", key["private"])
    print("public:", key["public"])
