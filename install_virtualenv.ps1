# install_virtualenv.ps1

# Install pip if not installed
if (-Not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "Installing pip..."
    Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
    python get-pip.py
    Remove-Item -Path "get-pip.py"
}

# Install virtualenv if not installed
if (-Not (Get-Command virtualenv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing virtualenv..."
    pip install virtualenv
}

# Create and activate virtual environment
if (-Not (Test-Path "./my_project_env")) {
    Write-Host "Creating virtual environment..."
    python -m venv my_project_env
}

Write-Host "Activating virtual environment..."
& "./my_project_env/Scripts/Activate"

# Install required packages
Write-Host "Installing required packages..."
pip install pygame
