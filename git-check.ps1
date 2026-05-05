chcp 65001 >nul 2>nul

Write-Host "=== Git + gh 环境检测 ==="

# Git
$git = "C:\Users\mengdejun\.qclaw\tools\git\cmd\git.exe"
if (Test-Path $git) {
    $v = & $git --version 2>&1 | Select-Object -First 1
    Write-Host "Git: $v"
    Write-Host "Path: $git"
} else {
    Write-Host "Git: 未找到"
}

# gh
$ghCmd = Get-Command gh -ErrorAction SilentlyContinue
if ($ghCmd) {
    Write-Host "gh CLI: $($ghCmd.Source)"
} else {
    Write-Host "gh CLI: 未安装"
}

# gh auth
& gh auth status 2>&1

# SSH key
$sshDir = Join-Path $env:USERPROFILE ".ssh"
Write-Host ""
Write-Host "SSH dir: $sshDir"
if (Test-Path $sshDir) {
    $keys = Get-ChildItem $sshDir -Filter "*.pub" -ErrorAction SilentlyContinue
    foreach ($k in $keys) { Write-Host "  Key: $($k.Name)" }
} else {
    Write-Host "SSH dir: 不存在"
}