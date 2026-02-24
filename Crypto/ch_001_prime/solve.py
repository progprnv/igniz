#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
import sympy

# Read public key
with open('pubkey.pem', 'r') as f:
    pubkey = RSA.import_key(f.read())

n = pubkey.n
e = pubkey.e

print(f"[*] Public Key Parameters:")
print(f"    n = {n}")
print(f"    e = {e}")
print(f"    n bit length: {n.bit_length()}")

# Read ciphertext
with open('flag.enc', 'r') as f:
    lines = f.read().strip().split('\n')
    ciphertext_hex = lines[1]

ciphertext = int(ciphertext_hex, 16)
print(f"\n[*] Ciphertext: {ciphertext_hex}")

# Factor n
print(f"\n[*] Attempting to factor n...")
factors = sympy.factorint(n)
print(f"[+] Factorization complete!")
print(f"    Factors: {factors}")

# Extract p and q
p = list(factors.keys())[0]
q = list(factors.keys())[1] if len(factors) > 1 else factors[p] // p

print(f"\n[*] Prime factors:")
print(f"    p = {p}")
print(f"    q = {q}")

# Compute private exponent d
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)  # Using Python 3.8+ modular inverse

print(f"\n[*] Computing private exponent:")
print(f"    φ(n) = {phi}")
print(f"    d = {d}")

# Decrypt the message
plaintext_int = pow(ciphertext, d, n)
plaintext = long_to_bytes(plaintext_int).decode()

print(f"\n[+] Decrypted Flag:")
print(f"    {plaintext}")
