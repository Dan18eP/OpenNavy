# ==============================================================================
# HACKATHON LOCAL SERVER LAUNCHER: GEMMA 4 + CLOUDFLARE TUNNEL
# ==============================================================================
# Este script inicia Ollama con configuración de alta concurrencia, CORS abierto,
# mantiene el modelo caliente en memoria y levanta un túnel público seguro con Cloudflare.
# ==============================================================================

param (
    [string]$Model = "gemma4:e4b",
    [switch]$EnableIGPU = $false
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "       🚀 INICIANDO SERVIDOR GEMMA 4 PARA HACKATHON             " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Variables de entorno de rendimiento y red
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_ORIGINS = "*"
$env:OLLAMA_KEEP_ALIVE = "-1"        # Mantiene el modelo en RAM/VRAM indefinidamente
$env:OLLAMA_NUM_PARALLEL = "2"       # Permite 2 peticiones concurrentes simultáneas

if ($EnableIGPU) {
    Write-Host "[INFO] Habilitando soporte para GPU integrada (Vulkan)..." -ForegroundColor Yellow
    $env:OLLAMA_IGPU_ENABLE = "1"
}

# 2. Verificar o iniciar demonio de Ollama
$ollamaProc = Get-Process -Name "*ollama*" -ErrorAction SilentlyContinue
if (-not $ollamaProc) {
    Write-Host "[1/3] Levantando proceso demonio de Ollama..." -ForegroundColor Green
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Minimized
    Start-Sleep -Seconds 3
} else {
    Write-Host "[1/3] Demonio de Ollama ya está activo en segundo plano." -ForegroundColor Green
}

# 3. Pre-cargar el modelo seleccionado en memoria (Warm-up)
Write-Host "[2/3] Pre-calentando modelo '$Model' en memoria (cero latencia inicial)..." -ForegroundColor Yellow
try {
    $warmupPayload = @{
        model = $Model
        keep_alive = -1
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $warmupPayload -ContentType "application/json" -TimeoutSec 30
    Write-Host "      Modelo '$Model' cargado exitosamente en RAM/VRAM." -ForegroundColor Green
} catch {
    Write-Host "      [AVISO] No se pudo pre-cargar inmediatamente: $_" -ForegroundColor DarkYellow
}

# 4. Obtener IP local (como opción B para la misma red)
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch '^127\.' -and $_.IPAddress -notmatch '^169\.' }).IPAddress | Select-Object -First 1
Write-Host "`n-----------------------------------------------------------------" -ForegroundColor Gray
Write-Host " [OPCION RED LOCAL] IP interna: http://$($localIp):11434" -ForegroundColor Cyan
Write-Host "-----------------------------------------------------------------" -ForegroundColor Gray

# 5. Iniciar Cloudflare Tunnel (Opción A recomendada contra AP Isolation)
Write-Host "[3/3] Levantando tunel Cloudflare para acceso HTTPS público..." -ForegroundColor Yellow
Write-Host "Copia la URL https://...trycloudflare.com que se mostrará a continuación`ny compártela con todo tu equipo para configurar el backend/frontend:`n" -ForegroundColor Green

# Asegurar cloudflared en PATH
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$binPath = Join-Path (Split-Path -Parent $scriptDir) "bin"
if (Test-Path (Join-Path $binPath "cloudflared.exe")) {
    $env:PATH = "$binPath;$env:PATH"
}

if (Get-Command cloudflared -ErrorAction SilentlyContinue) {
    cloudflared tunnel --url http://localhost:11434
} else {
    Write-Host "[ERROR] No se encontró cloudflared.exe. Por favor verifica la carpeta bin/." -ForegroundColor Red
}
