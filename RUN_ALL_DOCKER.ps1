#!/usr/bin/env powershell
# EncryptCTF 2019 - Run All Services Using Docker
# This script starts all Docker services for the CTF challenges

$projectRoot = "c:\Users\kannapi64x\Desktop\igniz"
Set-Location $projectRoot

Write-Host @"
╔═══════════════════════════════════════════════════════════════╗
║         EncryptCTF 2019 - Docker Services Launcher            ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Services to start
$services = @(
    @{ name = "Main CTF"; path = "."; port = "4000" },
    @{ name = "50_Slash_Slash"; path = "web\50_Slash_Slash"; port = "5000" },
    @{ name = "75_env"; path = "web\75_env"; port = "5001" },
    @{ name = "repeaaaaaat"; path = "web\repeaaaaaat"; port = "5002" },
    @{ name = "Sweeeeeeeet"; path = "web\Sweeeeeeeet"; port = "5003" },
    @{ name = "vault"; path = "web\vault"; port = "5004" },
    @{ name = "ham-me-baby"; path = "Misc\ham-me-baby"; port = "6969" }
)

Write-Host "`n[*] Stopping any existing containers..." -ForegroundColor Yellow
docker-compose down 2>$null
Get-ChildItem -Path "web", "Misc" -Recurse -Filter "docker-compose.yml" | ForEach-Object {
    Push-Location (Split-Path $_.FullName)
    docker-compose down 2>$null
    Pop-Location
}

Write-Host "`n[*] Starting Docker services..." -ForegroundColor Yellow

$startedServices = @()
$failedServices = @()

foreach ($service in $services) {
    Write-Host "`n[+] Starting: $($service.name) (Port: $($service.port))" -ForegroundColor Green
    
    Push-Location $service.path
    
    if (Test-Path "docker-compose.yml") {
        try {
            $output = docker-compose up -d 2>&1
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "    [OK] Started successfully" -ForegroundColor Green
                $startedServices += $service
            } else {
                Write-Host "    [ERROR] Failed to start" -ForegroundColor Red
                Write-Host "    $output" -ForegroundColor DarkRed
                $failedServices += $service
            }
        } catch {
            Write-Host "    [ERROR] Exception: $_" -ForegroundColor Red
            $failedServices += $service
        }
    } else {
        Write-Host "    [SKIP] No docker-compose.yml found" -ForegroundColor Yellow
    }
    
    Pop-Location
    Start-Sleep -Seconds 2
}

# Summary
Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║                      DEPLOYMENT SUMMARY                        ║
╚═══════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n[+] Successfully Started Services:" -ForegroundColor Green
foreach ($service in $startedServices) {
    Write-Host "  > $($service.name) - http://localhost:$($service.port)" -ForegroundColor Green
}

if ($failedServices.Count -gt 0) {
    Write-Host "`n[-] Failed Services:" -ForegroundColor Red
    foreach ($service in $failedServices) {
        Write-Host "  > $($service.name)" -ForegroundColor Red
    }
}

Write-Host "`n[*] Current Running Containers:" -ForegroundColor Yellow
docker ps --format "table {{.Names}}`t{{.Status}}`t{{.Ports}}"

Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║                      QUICK REFERENCE                           ║
╚═══════════════════════════════════════════════════════════════╝

Access Started Services:
"@ -ForegroundColor Cyan

foreach ($service in $startedServices) {
    Write-Host "  → $($service.name): http://localhost:$($service.port)" -ForegroundColor Cyan
}

Write-Host @"

Useful Commands:
  docker-compose ps                 # Check service status
  docker-compose logs -f            # View logs
  docker-compose down               # Stop all services
  docker ps                         # List running containers
  docker logs <container-name>      # View specific container logs

To stop all services:
  docker-compose down -v            # Remove volumes too
"@ -ForegroundColor Gray

Write-Host "`n[+] Docker setup complete!" -ForegroundColor Green
