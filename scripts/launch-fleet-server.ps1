# ==============================================================================
# OPENNAVY: MASTER FLEET SERVER LAUNCHER (LAN & GEMMA 4 SERVER)
# ==============================================================================
# Configura la maquina de Daniel como el servidor central de inferencia soberana
# y orquestador de red local para la tripulacion (Dylan Gamero y Brandon Carranza).
# ==============================================================================

param (
    [string]$Model = "gemma4:e4b",
    [switch]$EnableIGPU = $false,
    [switch]$NoBrowser = $false
)

Clear-Host
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "       OPENNAVY: LAN FLEET SERVER & GEMMA 4 ENGINE               " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Detectar IP de Red Local (Wi-Fi / LAN)
$localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { 
    $_.IPAddress -notmatch '^127\.' -and $_.IPAddress -notmatch '^169\.' -and $_.IPAddress -notmatch '^192\.168\.64\.'
}).IPAddress | Select-Object -First 1

if (-not $localIp) {
    $localIp = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notmatch '^127\.' -and $_.IPAddress -notmatch '^169\.' }).IPAddress | Select-Object -First 1
}
if (-not $localIp) { $localIp = "127.0.0.1" }

Write-Host "`n[PASO 1/5] Red Local Detectada: IP $localIp" -ForegroundColor Green

# 2. Configurar Entorno de Red de Ollama
$env:OLLAMA_HOST = "0.0.0.0:11434"
$env:OLLAMA_ORIGINS = "*"
$env:OLLAMA_KEEP_ALIVE = "-1"
$env:OLLAMA_NUM_PARALLEL = "4"

if ($EnableIGPU) {
    Write-Host "[INFO] Habilitando soporte iGPU (Vulkan)..." -ForegroundColor Yellow
    $env:OLLAMA_IGPU_ENABLE = "1"
}

# 3. Iniciar Demonio de Ollama si no esta activo
$ollamaProc = Get-Process -Name "*ollama*" -ErrorAction SilentlyContinue
if (-not $ollamaProc) {
    Write-Host "[PASO 2/5] Iniciando demonio de Ollama en 0.0.0.0:11434..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Minimized
    Start-Sleep -Seconds 3
} else {
    Write-Host "[PASO 2/5] Demonio Ollama activo en segundo plano." -ForegroundColor Green
}

# 4. Pre-calentar Modelo Gemma 4 (Evitar Cold-Start en Demo)
Write-Host "[PASO 3/5] Pre-calentando modelo '$Model' en memoria..." -ForegroundColor Yellow
try {
    $warmPayload = @{
        model = $Model
        prompt = "OpenNavy system online."
        stream = $false
        options = @{ num_predict = 5 }
    } | ConvertTo-Json

    $warmRes = Invoke-RestMethod -Method Post -Uri "http://localhost:11434/api/generate" -Body $warmPayload -ContentType "application/json" -TimeoutSec 35
    Write-Host "           Modelo '$Model' caliente y residente en VRAM/RAM." -ForegroundColor Green
} catch {
    Write-Host "           [AVISO] No se pudo pre-calentar de inmediato: $_" -ForegroundColor DarkYellow
}

# 5. Inicializar y Sembrar Base de Datos SQLite
Write-Host "[PASO 4/5] Verificando base de datos y siembra automatica de OpenNavy..." -ForegroundColor Yellow
$seedCmd = "import sys; sys.path.insert(0, 'backend'); from app.core.database import init_db; init_db(); from app.core.seeder import seed_opennavy_repo; seed_opennavy_repo()"
python -c $seedCmd

# 6. Levantar Servidores FastAPI y Vite
Write-Host "[PASO 5/5] Levantando servicios de red local..." -ForegroundColor Green

# Lanzar FastAPI Backend en background
$backendCmd = "python -m uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Write-Host '--- OPENNAVY BACKEND SERVER (Port 8000) ---' -ForegroundColor Cyan; $backendCmd" -WindowStyle Normal

# Lanzar Vite Frontend en background
$frontendCmd = "npm run dev --prefix frontend -- --host 0.0.0.0 --port 3000"
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Write-Host '--- OPENNAVY FRONTEND COCKPIT (Port 3000) ---' -ForegroundColor Green; $frontendCmd" -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "`n=================================================================" -ForegroundColor Cyan
Write-Host "       OPENNAVY ESTA OPERATIVO EN RED LOCAL                      " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host " En tu laptop (Daniel):" -ForegroundColor White
Write-Host "   - Cockpit Web:       http://localhost:3000" -ForegroundColor Cyan
Write-Host "   - Backend Swagger:   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`n Para compartir con Dylan y Brandon (Misma Wi-Fi):" -ForegroundColor White
Write-Host "   - Cockpit Web:       http://$($localIp):3000" -ForegroundColor Yellow
Write-Host "   - Sonar WebSocket:   ws://$($localIp):8000/api/v1/sonar/ws/sonar" -ForegroundColor Yellow
Write-Host "   - Ollama API:        http://$($localIp):11434" -ForegroundColor Yellow
Write-Host "=================================================================`n" -ForegroundColor Cyan

if (-not $NoBrowser) {
    Start-Process "http://localhost:3000"
}
