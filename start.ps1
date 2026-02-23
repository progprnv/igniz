###############################################################
# encryptCTF 2019 - Quick Start Script (Windows)
#
# This script builds and starts all CTF services + CTFd.
# After running, visit http://localhost:8000 to configure CTFd,
# then run setup_ctfd.py to import all challenges.
###############################################################

Write-Host ""
Write-Host "  ======================================================" -ForegroundColor Cyan
Write-Host "           encryptCTF 2019 - Deployment                  " -ForegroundColor Cyan
Write-Host "  ======================================================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
try {
    docker version | Out-Null
} catch {
    Write-Host "ERROR: Docker is not installed or not running." -ForegroundColor Red
    Write-Host "Please install Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Detect compose command
$composeCmd = $null
try {
    docker compose version | Out-Null
    $composeCmd = "docker compose"
} catch {
    try {
        docker-compose version | Out-Null
        $composeCmd = "docker-compose"
    } catch {
        Write-Host "ERROR: Docker Compose is not available." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[1/3] Building and starting all containers..." -ForegroundColor Yellow
Write-Host "       This may take several minutes on first run." -ForegroundColor Gray
Write-Host ""

if ($composeCmd -eq "docker compose") {
    docker compose up -d --build
} else {
    docker-compose up -d --build
}

Write-Host ""
Write-Host "[2/3] Waiting for CTFd to become ready..." -ForegroundColor Yellow

$ready = $false
for ($i = 1; $i -le 60; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 302) {
            Write-Host "       CTFd is ready!" -ForegroundColor Green
            $ready = $true
            break
        }
    } catch {}
    Start-Sleep -Seconds 2
}

if (-not $ready) {
    Write-Host "       WARNING: CTFd may not be ready yet. Check: docker logs ctfd" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Setup Instructions" -ForegroundColor Yellow
Write-Host ""
Write-Host "  ======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Open " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Green -NoNewline; Write-Host " in your browser"
Write-Host "  2. Complete the CTFd setup wizard:"
Write-Host "     - Set admin username & password"
Write-Host "     - CTF Name: encryptCTF 2019"
Write-Host "     - Mode: Jeopardy"
Write-Host ""
Write-Host "  3. Generate an API token:"
Write-Host "     Admin Panel -> Settings -> Access Tokens -> Generate"
Write-Host ""
Write-Host "  4. Import all challenges:"
Write-Host "     pip install requests" -ForegroundColor Green
Write-Host "     python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN" -ForegroundColor Green
Write-Host ""
Write-Host "     To set connection info to your server IP:" -ForegroundColor Gray
Write-Host "     python setup_ctfd.py --url http://localhost:8000 --token YOUR_TOKEN --host YOUR_IP" -ForegroundColor Green
Write-Host ""
Write-Host "  ======================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Challenge Services:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Challenge              Port     Category"
Write-Host "  ---------------------  -------  ----------"
Write-Host "  CTFd Scoreboard        8000     Platform"
Write-Host "  pwn0                   1234     Pwn"
Write-Host "  pwn1                   2345     Pwn"
Write-Host "  pwn2                   3456     Pwn"
Write-Host "  pwn3                   4567     Pwn"
Write-Host "  pwn4                   5678     Pwn"
Write-Host "  Slash Slash            5000     Web"
Write-Host "  repeaaaaaat            5050     Web"
Write-Host "  env                    6060     Web"
Write-Host "  ham-me-baby            6969     Misc"
Write-Host "  crackme03              7777     RE"
Write-Host "  Sweeeeeeeet           8888     Web"
Write-Host "  vault                  9090     Web"
Write-Host ""
Write-Host "  All services are running! Happy hacking!" -ForegroundColor Green
