"""
encryptCTF 2019 — CTFd Challenge Auto-Importer
================================================

This script automatically creates all challenges in CTFd via its REST API.
It also uploads downloadable files for static challenges.

Requirements:
    pip install requests

Usage:
    1. Start the platform:   docker-compose up -d --build
    2. Visit http://localhost:8000 and complete the initial CTFd setup wizard:
       - Admin username/password
       - CTF name: encryptCTF 2019
       - Choose "Jeopardy" mode
    3. Generate an API token: Admin Panel > Settings > Access Tokens > Generate
    4. Run this script:
         python setup_ctfd.py --url http://localhost:8000 --token <YOUR_TOKEN>
"""

import argparse
import json
import os
import sys
import requests


# ---------------------------------------------------------------------------
# CTFd API helper
# ---------------------------------------------------------------------------
class CTFdAPI:
    def __init__(self, base_url: str, token: str):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        })

    def create_challenge(self, name, category, description, value, flag,
                         connection_info=None, challenge_type="standard",
                         state="visible"):
        data = {
            "name": name,
            "category": category,
            "description": description,
            "value": value,
            "type": challenge_type,
            "state": state,
        }
        if connection_info:
            data["connection_info"] = connection_info

        resp = self.session.post(f"{self.base}/api/v1/challenges", json=data)
        resp.raise_for_status()
        chal = resp.json()["data"]
        chal_id = chal["id"]
        print(f"  [+] Created challenge #{chal_id}: {name} ({category}, {value} pts)")

        # Add flag
        flag_data = {
            "challenge_id": chal_id,
            "content": flag,
            "type": "static",
        }
        resp2 = self.session.post(f"{self.base}/api/v1/flags", json=flag_data)
        resp2.raise_for_status()

        return chal_id

    def upload_file(self, chal_id, filepath):
        """Upload a file and attach it to a challenge."""
        # Use a separate headers dict without Content-Type (requests sets multipart boundary)
        headers = {"Authorization": self.session.headers["Authorization"]}
        with open(filepath, "rb") as f:
            files = {"file": (os.path.basename(filepath), f)}
            data = {"challenge_id": chal_id, "type": "challenge"}
            resp = requests.post(
                f"{self.base}/api/v1/files",
                files=files,
                data=data,
                headers=headers,
            )
        resp.raise_for_status()
        print(f"       Uploaded: {os.path.basename(filepath)}")

    def add_hint(self, chal_id, content, cost=0):
        data = {
            "challenge_id": chal_id,
            "content": content,
            "cost": cost,
        }
        resp = self.session.post(f"{self.base}/api/v1/hints", json=data)
        resp.raise_for_status()


# ---------------------------------------------------------------------------
# Challenge Definitions
# ---------------------------------------------------------------------------
# BASE is the directory containing this script (repo root)
BASE = os.path.dirname(os.path.abspath(__file__))
HOST = "YOUR_SERVER_IP"  # Replace with your server's IP/domain

CHALLENGES = [
    # =================================================================
    #  CRYPTO
    # =================================================================
    {
        "name": "AEeeeeS",
        "category": "Crypto",
        "value": 75,
        "flag": "IGNIZ{3Y3S_4R3_0N_A3S_3CB!}",
        "description": (
            "He encrypted the flag using AES ECB.\n\n"
            "The key he gave was:\n"
            "`110100001010100111001101110001011101000010100000110001"
            "0110011000101001011000100111100101110100011001010110101"
            "10110010101111001`\n\n"
            "Is he mad?\n\n"
            "Ciphertext:\n"
            "`e31c491719831e262b84fa92e3973240ec7d3952814fa465f4de7e009b3d5a89`"
        ),
        "files": [
            os.path.join(BASE, "Crypto", "AEeeeeS", "Challenge_Description.txt"),
            os.path.join(BASE, "Crypto", "AEeeeeS", "ciphertext.txt"),
        ],
    },
    {
        "name": "(TopNOTCH)SA",
        "category": "Crypto",
        "value": 150,
        "flag": "IGNIZ{1%_0F_1%}",
        "description": (
            "I encrypted the flag with RSA... but the primes might be a little small. "
            "Can you break it?\n\n"
            "You are given the encrypted flag and the public key."
        ),
        "files": [
            os.path.join(BASE, "Crypto", "(TopNOTCH)SA", "flag.enc"),
            os.path.join(BASE, "Crypto", "(TopNOTCH)SA", "encrypt.py"),
        ],
    },
    {
        "name": "hard_looks",
        "category": "Crypto",
        "value": 50,
        "flag": "IGNIZ{W45_17_H4RD_3N0UGH?!}",
        "description": (
            "This cipher looks hard... but is it really?\n\n"
            "Dashes and underscores — what could they mean?"
        ),
        "files": [
            os.path.join(BASE, "Crypto", "hard_looks", "hardLooks.txt"),
        ],
    },
    {
        "name": "Julius,Q2Flc2FyCg==",
        "category": "Crypto",
        "value": 50,
        "flag": "IGNIZ{3T_7U_BRU73?!}",
        "description": (
            "Et tu, Brute?\n\n"
            "Julius Caesar liked to keep secrets. "
            "Maybe the challenge name itself is a hint..."
        ),
        "files": [
            os.path.join(BASE, "Crypto", "Julius,Q2Flc2FyCg==", "flag.enc"),
        ],
    },
    {
        "name": "RSA Baby",
        "category": "Crypto",
        "value": 100,
        "flag": "IGNIZ{74K1NG_B4BY_S73PS}",
        "description": (
            "Taking baby steps with RSA.\n\n"
            "I encrypted the flag but left something behind... "
            "Can you figure out what?"
        ),
        "files": [
            os.path.join(BASE, "Crypto", "RSA_Baby", "flag.enc"),
            os.path.join(BASE, "Crypto", "RSA_Baby", "encrypt.py"),
        ],
    },

    # =================================================================
    #  FORENSICS
    # =================================================================
    {
        "name": "Get Schwifty",
        "category": "Forensics",
        "value": 150,
        "flag": "IGNIZ{wubba_lubba_dub_dub}",
        "description": (
            "Show me what you got!\n\n"
            "There are hidden files in this disk image. "
            "Find them and get the flag.\n\n"
            "**Note:** This challenge has 2 flags. Submit either one."
        ),
        "hints": [
            {"content": "Second flag: IGNIZ{alw4ys_d3lete_y0ur_f1les_c0mpletely}", "cost": 0},
        ],
    },
    {
        "name": "Journey to the Centre of the File 1",
        "category": "Forensics",
        "value": 75,
        "flag": "IGNIZ{w422up_b14tch3s}",
        "description": (
            "It's like a Russian nesting doll... but with archives.\n\n"
            "How deep does this go?"
        ),
    },
    {
        "name": "Journey to the Centre of the File 2",
        "category": "Forensics",
        "value": 150,
        "flag": "IGNIZ{f33ls_g00d_d0nt_it?}",
        "description": (
            "The sequel is always harder.\n\n"
            "More compression formats this time — zip, bzip2, gzip. "
            "Can your script handle them all?"
        ),
        "files": [
            os.path.join(BASE, "Forensics", "150_Journey_to_the_centre_of_the_file_2", "ziptunnel2"),
        ],
    },

    # =================================================================
    #  MISC
    # =================================================================
    {
        "name": "crack-jack",
        "category": "Misc",
        "value": 75,
        "flag": "IGNIZ{C4acK!ng_7h3_Uncr4ck4bl3}",
        "description": (
            "Can you crack the password?\n\n"
            "Here's the encrypted password and a wordlist. Good luck!"
        ),
        "files": [
            os.path.join(BASE, "Misc", "crack-jack", "password.txt"),
            os.path.join(BASE, "Misc", "crack-jack", "wordlist.txt"),
        ],
    },
    {
        "name": "ham-me-baby",
        "category": "Misc",
        "value": 150,
        "flag": "IGNIZ{1t_w4s_h4rd_th4n_1_th0ught}",
        "description": (
            "Hamming it up!\n\n"
            "Connect to the server and fix the Hamming(7,4) codes. "
            "Get 100 in a row and the flag is yours."
        ),
        "connection_info": f"nc {HOST} 6969",
    },

    # =================================================================
    #  PWN
    # =================================================================
    {
        "name": "pwn0",
        "category": "Pwn",
        "value": 50,
        "flag": "IGNIZ{L3t5_R4!53_7h3_J05H}",
        "description": (
            "Baby's first buffer overflow.\n\n"
            "Can you change the variable to get the flag?"
        ),
        "connection_info": f"nc {HOST} 1234",
        "files": [
            os.path.join(BASE, "pwn", "x86", "pwn0", "pwn0"),
            os.path.join(BASE, "pwn", "x86", "pwn0", "pwn0.c"),
        ],
    },
    {
        "name": "pwn1",
        "category": "Pwn",
        "value": 100,
        "flag": "IGNIZ{Buff3R_0v3rfl0W5_4r3_345Y}",
        "description": (
            "Classic ret2func.\n\n"
            "There's a hidden function that gives you a shell. "
            "Can you redirect execution?"
        ),
        "connection_info": f"nc {HOST} 2345",
        "files": [
            os.path.join(BASE, "pwn", "x86", "pwn1", "pwn1"),
            os.path.join(BASE, "pwn", "x86", "pwn1", "pwn1.c"),
        ],
    },
    {
        "name": "pwn2",
        "category": "Pwn",
        "value": 150,
        "flag": "IGNIZ{N!c3_j0b_jump3R}",
        "description": (
            "Time to inject some shellcode.\n\n"
            "There's a handy gadget in the binary. Can you use it?"
        ),
        "connection_info": f"nc {HOST} 3456",
        "files": [
            os.path.join(BASE, "pwn", "x86", "pwn2", "pwn2"),
            os.path.join(BASE, "pwn", "x86", "pwn2", "pwn2.c"),
        ],
    },
    {
        "name": "pwn3",
        "category": "Pwn",
        "value": 200,
        "flag": "IGNIZ{70_7h3_C3nt3R_0f_L!bC}",
        "description": (
            "Return to libc.\n\n"
            "No useful functions in the binary this time. "
            "You'll need to use the C library itself."
        ),
        "connection_info": f"nc {HOST} 4567",
        "files": [
            os.path.join(BASE, "pwn", "x86", "pwn3", "pwn3"),
            os.path.join(BASE, "pwn", "x86", "pwn3", "pwn3.c"),
        ],
    },
    {
        "name": "pwn4",
        "category": "Pwn",
        "value": 250,
        "flag": "IGNIZ{Y0u_4R3_7h3_7ru3_King_0f_53v3n_KingD0ms}",
        "description": (
            "Format string exploitation.\n\n"
            "The program trusts your input a little too much. "
            "Can you overwrite a GOT entry?"
        ),
        "connection_info": f"nc {HOST} 5678",
        "files": [
            os.path.join(BASE, "pwn", "x86", "pwn4", "pwn4"),
            os.path.join(BASE, "pwn", "x86", "pwn4", "pwn4.c"),
        ],
    },

    # =================================================================
    #  REVERSE ENGINEERING
    # =================================================================
    {
        "name": "crackme01",
        "category": "Reverse Engineering",
        "value": 75,
        "flag": "IGNIZ{gdb_or_r2?}",
        "description": (
            "A simple crackme.\n\n"
            "Find the correct key to unlock the flag. "
            "GDB or radare2 — your choice."
        ),
        "files": [
            os.path.join(BASE, "re", "crackme01", "crackme01"),
        ],
    },
    {
        "name": "crackme02",
        "category": "Reverse Engineering",
        "value": 100,
        "flag": "IGNIZ{Algorithms-not-easy}",
        "description": (
            "Another crackme, but this time with XOR.\n\n"
            "Find the right username and password to decrypt the flag."
        ),
        "files": [
            os.path.join(BASE, "re", "crackme02", "crackme02"),
        ],
    },
    {
        "name": "crackme03",
        "category": "Reverse Engineering",
        "value": 200,
        "flag": "IGNIZ{B0mB_D!ffu53d}",
        "description": (
            "Defuse the bomb!\n\n"
            "5 stages, 5 inputs. Get them all right or BOOM. "
            "Connect to the server and solve it."
        ),
        "connection_info": f"nc {HOST} 7777",
        "files": [
            os.path.join(BASE, "re", "crackme03", "crackme03"),
        ],
    },

    # =================================================================
    #  WEB
    # =================================================================
    {
        "name": "Slash Slash",
        "category": "Web",
        "value": 50,
        "flag": "IGNIZ{comments_&_indentations_makes_johnny_a_good_programmer}",
        "description": (
            "A simple web challenge.\n\n"
            "Comments are a programmer's best friend... or worst enemy."
        ),
        "connection_info": f"http://{HOST}:5000",
    },
    {
        "name": "env",
        "category": "Web",
        "value": 75,
        "flag": "IGNIZ{v1rtualenvs_4re_c00l}",
        "description": (
            "Virtualenvs are cool.\n\n"
            "The server knows what time it is. Do you?"
        ),
        "connection_info": f"http://{HOST}:6060",
    },
    {
        "name": "repeaaaaaat",
        "category": "Web",
        "value": 150,
        "flag": "IGNIZ{!nj3c7!0n5_4r3_b4D}",
        "description": (
            "What's in a template?\n\n"
            "The server repeats what you say... but does it do more than that?"
        ),
        "connection_info": f"http://{HOST}:5050",
        "hints": [
            {"content": "Server-Side Template Injection (SSTI)", "cost": 50},
        ],
    },
    {
        "name": "Sweeeeeeeet",
        "category": "Web",
        "value": 100,
        "flag": "IGNIZ{4lwa4y5_Ch3ck_7h3_c00ki3s}",
        "description": (
            "Something sweet is hidden in the cookies.\n\n"
            "Check your browser's cookie jar carefully."
        ),
        "connection_info": f"http://{HOST}:8888",
    },
    {
        "name": "vault",
        "category": "Web",
        "value": 150,
        "flag": "IGNIZ{i_H4t3_inJ3c7i0n5}",
        "description": (
            "Break into the vault.\n\n"
            "The login page looks secure... or is it?"
        ),
        "connection_info": f"http://{HOST}:9090",
        "hints": [
            {"content": "SQL Injection", "cost": 50},
        ],
    },
]


def main():
    parser = argparse.ArgumentParser(description="Import encryptCTF challenges into CTFd")
    parser.add_argument("--url", default="http://localhost:8000",
                        help="CTFd base URL (default: http://localhost:8000)")
    parser.add_argument("--token", required=True,
                        help="CTFd API access token (from Admin > Settings > Access Tokens)")
    parser.add_argument("--host", default=None,
                        help="Server IP/hostname for connection info (default: localhost)")
    args = parser.parse_args()

    if args.host:
        global HOST
        HOST = args.host
        # Update connection_info in challenges
        for ch in CHALLENGES:
            if "connection_info" in ch:
                ch["connection_info"] = ch["connection_info"].replace("YOUR_SERVER_IP", HOST)

    api = CTFdAPI(args.url, args.token)

    print("=" * 60)
    print("  encryptCTF 2019 — Challenge Importer")
    print("=" * 60)
    print()

    success = 0
    failed = 0

    for ch in CHALLENGES:
        try:
            conn = ch.get("connection_info", "").replace("YOUR_SERVER_IP", args.host or "localhost")
            chal_id = api.create_challenge(
                name=ch["name"],
                category=ch["category"],
                description=ch["description"],
                value=ch["value"],
                flag=ch["flag"],
                connection_info=conn if conn else None,
            )

            # Upload files
            for fpath in ch.get("files", []):
                if os.path.exists(fpath):
                    api.upload_file(chal_id, fpath)
                else:
                    print(f"       [!] File not found: {fpath}")

            # Add hints
            for hint in ch.get("hints", []):
                api.add_hint(chal_id, hint["content"], hint.get("cost", 0))

            success += 1
        except Exception as e:
            print(f"  [!] FAILED: {ch['name']} — {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"  Done! {success} challenges created, {failed} failed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
