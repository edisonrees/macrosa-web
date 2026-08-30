# Start Macrosa local preview + cloudflared tunnel for firewall bypass review.
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "Starting HTTP server on http://127.0.0.1:8765 ..."
Start-Process -WindowStyle Minimized python -ArgumentList "-m","http.server","8765","--bind","127.0.0.1" -WorkingDirectory $root

Start-Sleep -Seconds 2

Write-Host "Starting cloudflared quick tunnel..."
Write-Host "Copy the trycloudflare.com URL from the output below into TUNNEL.md"
cloudflared tunnel --url http://127.0.0.1:8765
