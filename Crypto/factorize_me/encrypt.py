from Crypto.PublicKey import RSA
from Crypto.Util.number import *
import gmpy2
import os

flag = open("flag.txt",'rb')  # Open in binary mode

p = getPrime(128)
q = getPrime(128)
n = p*q
e = 65537
phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)

message = bytes_to_long(flag.read())

ciphertext = pow(message,e,n)
ciphertext_hex = hex(ciphertext)[2:]  # Convert to hex without '0x' prefix
encrypt = open("flag.enc",'w')

encrypt.write("ciphertext: \n" + ciphertext_hex)
encrypt.close()
flag.close()
pubkeyfile = open("pubkey.pem",'w')
pubkey = RSA.construct([n, e])  # long() not needed in Python 3
pubkeyfile.write(pubkey.exportKey('PEM').decode())
pubkeyfile.close()
