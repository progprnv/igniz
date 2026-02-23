#!/bin/bash
###############################################################
# encryptCTF 2019 — Quick Start Script
#
# This script builds and starts all CTF services + CTFd.
# After running, visit http://localhost:8000 to configure CTFd,
# then run setup_ctfd.py to import all challenges.
###############################################################

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════╗"
echo "║          encryptCTF 2019 — Deployment            ║"
echo "╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "ERROR: Docker Compose is not installed."
    exit 1
fi

# Detect compose command
if docker compose version &> /dev/null 2>&1; then
    COMPOSE="docker compose"
else
    COMPOSE="docker-compose"
fi

echo -e "${YELLOW}[1/3] Building and starting all containers...${NC}"
echo "       This may take several minutes on first run."
echo ""
$COMPOSE up -d --build

echo ""
echo -e "${YELLOW}[2/3] Waiting for CTFd to become ready...${NC}"
for i in $(seq 1 60); do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200\|302"; then
        echo -e "       ${GREEN}CTFd is ready!${NC}"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "       WARNING: CTFd may not be ready yet. Check 'docker logs ctfd'."
    fi
    sleep 2
done

echo ""
echo -e "${YELLOW}[3/3] Setup Instructions${NC}"
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "  1. Open ${GREEN}http://localhost:8000${NC} in your browser"
echo "  2. Complete the CTFd setup wizard:"
echo "     - Set admin username & password"
echo "     - CTF Name: encryptCTF 2019"
echo "     - Mode: Jeopardy"
echo ""
echo "  3. Generate an API token:"
echo "     Admin Panel → Settings → Access Tokens → Generate"
echo ""
echo "  4. Import all challenges:"
echo "     ${GREEN}pip install requests${NC}"
echo "     ${GREEN}python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN${NC}"
echo ""
echo "     To set connection info to your server IP:"
echo "     ${GREEN}python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN --host YOUR_IP${NC}"
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}Challenge Services:${NC}"
echo ""
echo "  ┌──────────────────────┬──────────┬────────────┐"
echo "  │ Challenge            │ Port     │ Category   │"
echo "  ├──────────────────────┼──────────┼────────────┤"
echo "  │ CTFd Scoreboard      │ 8000     │ Platform   │"
echo "  │ pwn0                 │ 1234     │ Pwn        │"
echo "  │ pwn1                 │ 2345     │ Pwn        │"
echo "  │ pwn2                 │ 3456     │ Pwn        │"
echo "  │ pwn3                 │ 4567     │ Pwn        │"
echo "  │ pwn4                 │ 5678     │ Pwn        │"
echo "  │ Slash Slash          │ 5000     │ Web        │"
echo "  │ repeaaaaaat          │ 5050     │ Web        │"
echo "  │ env                  │ 6060     │ Web        │"
echo "  │ ham-me-baby          │ 6969     │ Misc       │"
echo "  │ crackme03            │ 7777     │ RE         │"
echo "  │ Sweeeeeeeet         │ 8888     │ Web        │"
echo "  │ vault                │ 9090     │ Web        │"
echo "  └──────────────────────┴──────────┴────────────┘"
echo ""
echo -e "${GREEN}All services are running! Happy hacking! 🚩${NC}"
