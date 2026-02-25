#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
import gmpy2

print("="*80)
print("RSA BABY - CRACKING THE RSA ENCRYPTION")
print("="*80)

# Read the encrypted flag and RSA parameters
with open('flag.enc', 'r') as f:
    lines = f.read().strip().split('\n')
    ciphertext_hex = lines[1]
    n = int(lines[3])

ciphertext = int(ciphertext_hex, 16)

print(f"\n[*] Given parameters from flag.enc:")
print(f"    Ciphertext: {ciphertext_hex}")
print(f"    n = {n}")

# The key insight: q is left "behind" in the encrypt.py as a hint
# q = 9896984395151566492448748862139262345387297785144637332499966426571398040295087125558780121504834847289828037371643927199404615218623314326851473129699891
q = 9896984395151566492448748862139262345387297785144637332499966426571398040295087125558780121504834847289828037371643927199404615218623314326851473129699891

print(f"\n[*] Key insight - q is hardcoded in encrypt.py!")
print(f"    q = {q}")

# Factor n to get p
print(f"\n[*] Computing p from n/q:")
p = n // q
print(f"    p = {p}")
print(f"    Verification: p*q == n? {p*q == n}")

# Compute private exponent
print(f"\n[*] Computing private exponent d:")
e = 65537
phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)
print(f"    e = {e}")
print(f"    d = {d}")

# Decrypt the message
print(f"\n[*] Decrypting the ciphertext:")
plaintext_int = pow(ciphertext, d, n)
plaintext_bytes = long_to_bytes(plaintext_int)
plaintext = plaintext_bytes.decode('utf-8')

print(f"\n[+] DECRYPTED FLAG:")
print(f"    {plaintext}")
print(f"\n{'='*80}")
