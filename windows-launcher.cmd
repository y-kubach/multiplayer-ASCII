@echo off
where python3 > nul 2>&1
if %errorlevel% == 0 (
    python3 -m venv venv
    call venv\Scripts\activate
    where python3 > nul 2>&1
    pip install -r requirements.txt
    python start.py
) else (
    where python > nul 2>&1
    if %errorlevel% == 0 (
        python -m venv venv
        call venv\Scripts\activate
        where python3 > nul 2>&1
        pip install -r requirements.txt
        python start.py
    ) else (
        echo No python or python3 installation found
    )
)