#!/usr/bin/env powershell
# Rename all CTF challenges to obfuscated names to hide origin

$projectRoot = "c:\Users\kannapi64x\Desktop\igniz"
Set-Location $projectRoot

Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       Challenge Renaming - Hiding CTF Challenge Names         ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Mapping of old names to new obfuscated names
$renameMap = @{
    # CRYPTO CHALLENGES
    'Crypto/(TopNOTCH)SA' = 'Crypto/ch_001_prime'
    'Crypto/AEeeeeS' = 'Crypto/ch_002_cipher'
    'Crypto/hard_looks' = 'Crypto/ch_003_encoding'
    'Crypto/Julius,Q2Flc2FyCg==' = 'Crypto/ch_004_decode'
    'Crypto/RSA_Baby' = 'Crypto/ch_005_factory'
    
    # MISC CHALLENGES
    'Misc/crack-jack' = 'Misc/ch_006_pattern'
    'Misc/ham-me-baby' = 'Misc/ch_007_protocol'
    
    # WEB CHALLENGES
    'web/50_Slash_Slash' = 'web/ch_008_discovery'
    'web/75_env' = 'web/ch_009_temporal'
    'web/repeaaaaaat' = 'web/ch_010_inject'
    'web/Sweeeeeeeet' = 'web/ch_011_verify'
    'web/vault' = 'web/ch_012_login'
}

$successCount = 0
$failedCount = 0

Write-Host "`n[*] Starting rename operations...`n" -ForegroundColor Yellow

foreach ($oldPath in $renameMap.Keys) {
    $newPath = $renameMap[$oldPath]
    $oldFullPath = Join-Path $projectRoot $oldPath
    $newFullPath = Join-Path $projectRoot $newPath
    
    if (Test-Path $oldFullPath) {
        try {
            Write-Host "[→] $oldPath" -ForegroundColor Gray
            Write-Host "    → $newPath" -ForegroundColor Cyan
            
            # Rename using git to preserve history and handle special chars
            git mv $oldPath $newPath 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "    [OK] Renamed successfully" -ForegroundColor Green
                $successCount++
            } else {
                # Fallback to direct rename if git fails
                Move-Item $oldFullPath $newFullPath -Force
                Write-Host "    [OK] Renamed (fallback method)" -ForegroundColor Green
                $successCount++
            }
        } catch {
            Write-Host "    [ERROR] Failed: $_" -ForegroundColor Red
            $failedCount++
        }
    } else {
        Write-Host "[!] $oldPath not found" -ForegroundColor Yellow
    }
}

Write-Host "`n╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                     RENAME SUMMARY                            ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

Write-Host "`n[+] Successfully Renamed: $successCount" -ForegroundColor Green
Write-Host "[-] Failed Renames: $failedCount" -ForegroundColor Red

Write-Host "`n[*] Updating docker-compose.yml references..." -ForegroundColor Yellow

# Update docker-compose.yml files to reflect new service names
$dockerFiles = Get-ChildItem -Path "web", "Misc" -Recurse -Filter "docker-compose.yml"

foreach ($dockerFile in $dockerFiles) {
    $filePath = $dockerFile.FullName
    $content = Get-Content $filePath -Raw
    $originalContent = $content
    
    foreach ($oldService in $renameMap.Keys) {
        $oldName = Split-Path $oldService -Leaf
        $newName = Split-Path $renameMap[$oldService] -Leaf
        
        # Replace service names in docker-compose
        $content = $content -replace "container_name:\s*$oldName", "container_name: $newName"
        $content = $content -replace "service:\s*$oldName", "service: $newName"
    }
    
    if ($content -ne $originalContent) {
        Set-Content $filePath $content
        Write-Host "[OK] Updated: $filePath" -ForegroundColor Green
    }
}

Write-Host "`n[*] Git staging changes..." -ForegroundColor Yellow
git add . 2>&1 | Out-Null

Write-Host "`n[*] New Challenge Structure:" -ForegroundColor Yellow
Write-Host "`n  Crypto:" -ForegroundColor Cyan
Get-ChildItem -Path "Crypto" -Directory | ForEach-Object { Write-Host "    - $_" -ForegroundColor Green }

Write-Host "`n  Misc:" -ForegroundColor Cyan
Get-ChildItem -Path "Misc" -Directory | ForEach-Object { Write-Host "    - $_" -ForegroundColor Green }

Write-Host "`n  Web:" -ForegroundColor Cyan
Get-ChildItem -Path "web" -Directory | ForEach-Object { Write-Host "    - $_" -ForegroundColor Green }

Write-Host "`n  Pwn (UNCHANGED):" -ForegroundColor Cyan
Get-ChildItem -Path "pwn" -Directory -Recurse -MaxDepth 1 | ForEach-Object { Write-Host "    - $_" -ForegroundColor Green }

Write-Host @"

╔═══════════════════════════════════════════════════════════════╗
║                      NAMING MAP                               ║
╚═══════════════════════════════════════════════════════════════╝

CRYPTO:
  ch_001_prime     (previously: TopNOTCH)SA - RSA with small primes)
  ch_002_cipher    (previously: AEeeeeS - AES ECB decryption)
  ch_003_encoding  (previously: hard_looks - Binary encoding)
  ch_004_decode    (previously: Julius - Base64 + Caesar shift)
  ch_005_factory   (previously: RSA_Baby - RSA with known prime)

MISC:
  ch_006_pattern   (previously: crack-jack - Wordlist cracking)
  ch_007_protocol  (previously: ham-me-baby - Hamming(7,4) codes)

WEB:
  ch_008_discovery (previously: 50_Slash_Slash - Hidden endpoint)
  ch_009_temporal  (previously: 75_env - Time race condition)
  ch_010_inject    (previously: repeaaaaaat - SSTI)
  ch_011_verify    (previously: Sweeeeeeeet - Cookie manipulation)
  ch_012_login     (previously: vault - SQL injection)

PWN (UNCHANGED):
  x86/pwn0         Buffer overflow + stack check
  x86/pwn1         Return-to-function ROP
  x86/pwn2-4       Advanced exploitation

"@ -ForegroundColor Gray

Write-Host "[+] Rename operation complete!" -ForegroundColor Green
Write-Host "[!] Run 'git commit -m \"Obfuscate challenge names\"' to finalize" -ForegroundColor Yellow
