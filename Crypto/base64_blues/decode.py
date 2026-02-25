#!/usr/bin/env python3
import base64

flag = ""
ciphertext = base64.b64decode("YV9mYXLCk0tsd09td1pqbU9LVznClQ==").decode()
for char in ciphertext:
    flag += chr(ord(char) - 24)

print(flag)
