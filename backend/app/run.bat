@echo off
REM Batch file to start the KotchaApp backend and frontend servers.
REM Place this file in the root directory of your project 
REM (e.g., KotchaApp-49b5eba9cddcdc8b0b2e5fcf4d7a03f26a16100d/).

echo Starting KotchaApp services...
echo.

REM --- Start Backend Server ---
echo Starting FastAPI backend server...
cd backend
REM Optional: If you use a Python virtual environment located in the project root (e.g., named 'venv')
REM activate it. Adjust the path if your venv is elsewhere or named differently.
REM IF EXIST ..\venv\Scripts\activate.bat (
REM    echo Activating Python virtual environment...
REM    CALL ..\venv\Scripts\activate.bat
REM ) ELSE (
REM    echo Python virtual environment not found or not activated. Assuming dependencies are globally available.
REM )

REM Optional: Install/update Python dependencies
REM echo Installing/updating backend dependencies from requirements.txt...
REM pip install -r requirements.txt

REM Start Uvicorn server in a new window
REM The backend will be accessible at http://<your_computer_ip>:8000
start "Kotcha Backend" uvicorn app.main:app --host 0.0.0.0 --port 8000
echo Backend server starting in a new window.
cd ..
echo.

REM --- Start Frontend Server ---
echo Starting Vue.js frontend server...
cd kotcha

REM Optional: Install/update Node.js dependencies
REM echo Installing/updating frontend dependencies from package.json...
REM npm install

REM Start Vite dev server in a new window
REM (Assumes 'vite --host 0.0.0.0' is the 'dev' script in package.json)
REM The frontend will be accessible at http://<your_computer_ip>:<vite_port> (usually 5173)
start "Kotcha Frontend" npm run dev
echo Frontend server starting in a new window.
cd ..
echo.

echo =================================================================
echo Both servers are starting up in separate windows.
echo.
echo Access the backend API at: http://<your_computer_ip>:8000
echo Access the frontend application at: http://<your_computer_ip>:<vite_port> 
echo (Vite will show the exact port, usually 5173 or the next available)
echo.
echo Replace <your_computer_ip> with your actual local IP address.
echo Make sure your phone is on the same Wi-Fi network.
echo You might need to adjust firewall settings if you encounter issues.
echo =================================================================
echo.
pause
