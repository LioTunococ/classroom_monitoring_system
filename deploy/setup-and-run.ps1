param(
  [string]$Domain = "",
  [string]$Secret = "",
  [switch]$Https,
  [string]$Bind = "127.0.0.1",
  [int]$Port = 8000
)

# Ensure venv Python exists
$venvPython = Join-Path ".\.venv\Scripts" "python.exe"
if (!(Test-Path $venvPython)) { Write-Error "Virtualenv python not found at $venvPython"; exit 1 }

# Generate a strong secret if not provided
if (-not $Secret) {
  $Secret = & $venvPython -c "import secrets;print(secrets.token_urlsafe(64))"
}

# Base secure env
$env:DJANGO_DEBUG = "false"
$env:DJANGO_SECRET_KEY = $Secret
if ($Domain) { $env:DJANGO_ALLOWED_HOSTS = $Domain }

if ($Https.IsPresent -and $Https) {
  $env:DJANGO_SECURE_SSL_REDIRECT = "true"
  $env:DJANGO_HSTS_SECONDS = "31536000"
  $env:DJANGO_HSTS_INCLUDE_SUBDOMAINS = "true"
  $env:DJANGO_HSTS_PRELOAD = "true"
  # If you're behind a reverse proxy (Nginx/ELB), trust forwarded proto
  $env:DJANGO_SECURE_PROXY_SSL_HEADER = "true"
  if ($Domain) {
    # Accept multiple domains separated by comma
    $origins = ($Domain -split ",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" } | ForEach-Object { "https://$_" }
    $env:DJANGO_CSRF_TRUSTED_ORIGINS = ($origins -join ",")
  }
} else {
  Write-Warning "HTTPS is OFF. Use only for local pilot; cookies will be secure-only when DEBUG=false."
}

# Install deps, migrate, collectstatic
& $venvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Error "pip install failed"; exit 1 }

& $venvPython manage.py migrate
if ($LASTEXITCODE -ne 0) { Write-Error "migrate failed"; exit 1 }

& $venvPython manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) { Write-Error "collectstatic failed"; exit 1 }

# Deployment checks
& $venvPython manage.py check --deploy

# Start waitress (production WSGI server) bound to the chosen address
Write-Host ("Starting waitress on {0}:{1} ..." -f $Bind, $Port)
$listen = "$($Bind):$Port"
& .\.venv\Scripts\waitress-serve --listen=$listen cms.wsgi:application
