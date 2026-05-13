from toon import TOON
d = {"a":1, "b":[2,3], "c":{"d":True}}
enc = TOON.encode(d)
dec = TOON.decode(enc)
print(f"ENC: {enc}")
print(f"DEC: {dec}")
print(f"MATCH: {d == dec}")
