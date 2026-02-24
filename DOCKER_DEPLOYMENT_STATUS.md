# 🐳 EncryptCTF 2019 - Docker Deployment Summary

## Status Report (2026-02-24)

### Currently Running Services
```
repeaaaaaat: Up and running
```

**Note:** Docker container builds are in progress or have network connectivity issues pulling images from Docker Hub.

---

## Available Services & Ports

| Challenge | Type | Docker Status | Local Port | Access URL |
|-----------|------|---|---|---|
| Main CTF / HOSTING | Central | Building | 4000 | http://localhost:4000 |
| **50_Slash_Slash** | Web | Pending | 5000 | http://localhost:5000 |
| **75_env** | Web | Pending | 5001 | http://localhost:5001 |
| **repeaaaaaat** | Web | ✅ Running | 5002 | http://localhost:5002 |
| **Sweeeeeeeet** | Web | Pending | 5003 | http://localhost:5003 |
| **vault** | Web | Pending | 5004 | http://localhost:5004 |
| **ham-me-baby** | Misc | Pending | 6969 | Remote socket |

---

## Docker Setup Issues & Solutions

### Network Connectivity
Docker is experiencing TLS handshake timeouts when pulling images. This is usually due to:
- Slow/unstable internet connection
- Docker registry rate limiting
- Packet loss or network issues

### Solution Options

**Option 1: Wait & Retry**
```powershell
# Retry individual service
cd web\75_env
docker-compose up -d
```

**Option 2: Run Locally Without Docker**
Most challenges can run without Docker:
```bash
# Crypto challenges
python3 Crypto/AEeeeeS/solve.py

# PWN challenges (requires Linux)
gcc pwn/x86/pwn0/pwn0.c -o pwn0
gdb ./pwn0

# Web challenges (require Python/PHP/MySQL)
cd web/75_env/app
python3 application.py
```

**Option 3: Use WSL 2 with better networking**
Docker on WSL 2 often has better connectivity than Docker Desktop.

---

## Manually Starting Services

### Start individual services:
```powershell
# 75_env
cd web\75_env
docker-compose up -d

# Sweeeeeeeet
cd web\Sweeeeeeeet
docker-compose up -d

# vault (includes MySQL)
cd web\vault
docker-compose up -d

# ham-me-baby
cd Misc\ham-me-baby
docker-compose up -d
```

### Monitor build progress:
```powershell
docker-compose logs -f <service-name>
```

---

## Access Running Services

Once containers are up:

```powershell
# Test if service is responding
Invoke-WebRequest http://localhost:5002 -UseBasicParsing

# Or use curl
curl http://localhost:5002

# Access shell in container
docker exec -it <container-name> /bin/bash
```

---

## Useful Docker Commands

```powershell
# Check all services status
docker-compose ps

# View logs of specific service
docker-compose logs -f repeaaaaaat

# Stop all services
docker-compose down

# Remove images and volumes
docker-compose down -v

# Full cleanup
docker system prune -a -v
```

---

## Running Challenges Without Docker

If Docker is too slow, run challenges natively:

### Crypto Challenges
```powershell
cd Crypto/(TopNOTCH)SA
python3 -c "import gmpy2; print('Ready')"
```

### Web Challenges (Native)
```powershell
# Install Python dependencies
pip install flask requests

# Run Flask app directly
cd web\75_env\app
python3 application.py

# Then access: http://localhost:5000
```

### Pwn Challenges
```powershell
# WSL 2 or Ubuntu required
wsl gcc pwn/x86/pwn0/pwn0.c -o pwn0
wsl gdb ./pwn0
```

---

## Docker Desktop Settings to Improve Performance

1. **Increase allocated resources:**
   - Open Docker Desktop → Settings
   - Resources → Increase CPU, Memory, Disk
   - Recommended: 4+ CPUs, 4-8GB RAM, 30GB Disk

2. **Use WSL 2 backend:**
   - Settings → General → Enable WSL 2 (if not already)
   - Settings → Resources → WSL Integration

3. **Disable VPN/Proxy temporarily:**
   - Some VPNs interfere with Docker registry pulls

---

## What's Your Best Option?

✅ **Recommended Approach:**
1. **Try Docker first** (cleaner, isolated environment)
2. **If Docker fails:** Run challenges natively with Python/PHP
3. **For PWN challenges:** Use WSL 2 or native Linux VM

All challenges CAN be solved without Docker - it's just recommended for isolation.

---

## Next Steps

```powershell
# Check if Docker can pull fresh images
docker pull python:3

# If that works, retry the main compose:
cd c:\Users\kannapi64x\Desktop\igniz
docker-compose up -d

# If still failing, use native setup from UBUNTU_QUICK_START.md
```

