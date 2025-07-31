@echo off
setlocal enabledelayedexpansion

REM -- Check if python is installed --
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing Python...

    REM Download Python installer
    set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    set INSTALLER=python_installer.exe

    powershell -Command "Invoke-WebRequest -Uri %PYTHON_INSTALLER_URL% -OutFile %INSTALLER%"

    REM Install Python silently with pip, add to PATH for all users
    start /wait "" %INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

    del %INSTALLER%

    REM Refresh environment variables so python is in PATH for this session
    set "PATH=%PATH%;%LocalAppData%\Programs\Python\Python312\Scripts;%LocalAppData%\Programs\Python\Python312\"

    REM Wait a few seconds for installation to settle
    timeout /t 5 /nobreak >nul

    REM Verify Python install
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python installation failed. Please install manually.
        pause
        exit /b 1
    )
) else (
    echo Python found.
)

REM -- Install required packages --
echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install pyinstaller pillow

REM -- Build the executable --
echo.
echo Compiling executable with PyInstaller...
pyinstaller --noconsole --onefile --icon=avatar_icon.ico --add-data "CashMfinMoney-qrcode.png;." CashMfinMoneysProfileManager.py

echo.
echo Build complete! Your executable is in the "dist" folder.
pause
