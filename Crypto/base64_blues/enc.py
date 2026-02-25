#!/usr/bin/env python3
import base64

flag = "IGNIZ{3T_7U_BRU73?!}"
#flagb64 = flag.encode('base64')  <-- not used 
ciphertext = ""
for char in flag:
    ciphertext += chr(ord(char) + 24)

print(base64.b64encode(ciphertext.encode()).decode())
