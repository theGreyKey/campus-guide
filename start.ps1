$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$AppFile = Join-Path $ProjectRoot "app.py"
$Port = 8501

if (-not (Test-Path -LiteralPath $PythonExe)) {
    Write-Host "未找到虚拟环境：.venv" -ForegroundColor Yellow
    Write-Host "请先在项目根目录运行："
    Write-Host "python -m venv .venv"
    Write-Host ".\.venv\Scripts\Activate.ps1"
    Write-Host "pip install -r requirements.txt"
    exit 1
}

if (-not (Test-Path -LiteralPath $AppFile)) {
    Write-Host "未找到 app.py，请确认脚本位于项目根目录。" -ForegroundColor Red
    exit 1
}

Set-Location -LiteralPath $ProjectRoot

Write-Host "正在启动湖南大学金融科技导航系统..." -ForegroundColor Green
Write-Host "本地访问地址：http://localhost:$Port"
Write-Host "按 Ctrl+C 可停止服务。"

& $PythonExe -m streamlit run $AppFile --server.headless true --server.port $Port
