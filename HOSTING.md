# Hosting encryptCTF 2019

## Prerequisites

- **Docker** (with Docker Compose v2)
- **Python 3.6+** (for the challenge importer)
- **~4 GB RAM** recommended (for all containers)

## Quick Start

### 1. Launch Everything

**Windows (PowerShell):**
```powershell
cd encrypt-ctf-master
.\start.ps1
```

**Linux/macOS:**
```bash
cd encrypt-ctf-master
chmod +x start.sh
./start.sh
```

**Or manually:**
```bash
docker compose up -d --build
```

### 2. Configure CTFd

1. Open **http://localhost:8000** in your browser
2. Complete the setup wizard:
   - **Admin username & password** — choose something secure
   - **CTF Name:** `encryptCTF 2019`
   - **Mode:** Jeopardy
3. Go to **Admin Panel → Settings → Access Tokens → Generate**
4. Copy the generated token

### 3. Import Challenges

```bash
pip install requests
python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN_HERE
```

If hosting on a remote server, specify the public IP so players see correct connection info:
```bash
python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN --host 203.0.113.50
```

## Port Map

| Service          | Port  | Category | Protocol |
|------------------|-------|----------|----------|
| **CTFd**         | 8000  | Platform | HTTP     |
| pwn0             | 1234  | Pwn      | TCP      |
| pwn1             | 2345  | Pwn      | TCP      |
| pwn2             | 3456  | Pwn      | TCP      |
| pwn3             | 4567  | Pwn      | TCP      |
| pwn4             | 5678  | Pwn      | TCP      |
| Slash Slash      | 5000  | Web      | HTTP     |
| repeaaaaaat      | 5050  | Web      | HTTP     |
| env              | 6060  | Web      | HTTP     |
| ham-me-baby      | 6969  | Misc     | TCP      |
| crackme03        | 7777  | RE       | TCP      |
| Sweeeeeeeet     | 8888  | Web      | HTTP     |
| vault            | 9090  | Web      | HTTP     |

**Total ports needed:** 8000, 1234, 2345, 3456, 4567, 5678, 5000, 5050, 6060, 6969, 7777, 8888, 9090

## Challenge Categories (22 challenges)

| Category            | Count | Type                    |
|---------------------|-------|-------------------------|
| Crypto              | 5     | Static (downloadable)   |
| Forensics           | 3     | Static (downloadable)   |
| Misc                | 2     | 1 static + 1 networked  |
| Pwn                 | 5     | All networked           |
| Reverse Engineering | 3     | 2 static + 1 networked  |
| Web                 | 5     | All networked           |

## Firewall Rules

If hosting on a cloud server, open these ports:

```bash
# UFW example
sudo ufw allow 8000/tcp   # CTFd
sudo ufw allow 1234/tcp   # pwn0
sudo ufw allow 2345/tcp   # pwn1
sudo ufw allow 3456/tcp   # pwn2
sudo ufw allow 4567/tcp   # pwn3
sudo ufw allow 5678/tcp   # pwn4
sudo ufw allow 5000/tcp   # Slash Slash
sudo ufw allow 5050/tcp   # repeaaaaaat
sudo ufw allow 6060/tcp   # env
sudo ufw allow 6969/tcp   # ham-me-baby
sudo ufw allow 7777/tcp   # crackme03
sudo ufw allow 8888/tcp   # Sweeeeeeeet
sudo ufw allow 9090/tcp   # vault
```

## Management

```bash
# View running containers
docker compose ps

# View logs
docker compose logs -f ctfd
docker compose logs -f vault

# Restart a specific service
docker compose restart pwn0

# Stop everything
docker compose down

# Stop and remove all data (fresh start)
docker compose down -v
```

## Customization

### Change CTFd Version
Edit the `ctfd` service image tag in `docker-compose.yml`:
```yaml
image: ctfd/ctfd:3.7.0
```

### Add HTTPS (Production)
Put an nginx reverse proxy in front of CTFd with Let's Encrypt:
```bash
# Example with certbot
sudo apt install nginx certbot python3-certbot-nginx
```

### Adjust Challenge Points
Edit the `value` field for each challenge in `setup_ctfd.py` and re-run it (delete existing challenges in CTFd first).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Port already in use | Change the host port in `docker-compose.yml` (left side of `:`) |
| vault login doesn't work | Wait 30s for MariaDB to initialize, then retry |
| CTFd shows 502 | Wait for the database to start: `docker compose logs ctfd-db` |
| pwn challenges timeout | The Ubuntu 14.04 i386 images are large; give them time to build |
| `setup_ctfd.py` fails with 401 | Regenerate the API token in CTFd admin panel |
