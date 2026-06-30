@echo off
cd /d "%~dp0"
echo Starting Korea Japan Trend Dashboard...
echo Your browser will open automatically.
echo Close this window to stop the dashboard.
echo.
".venv\Scripts\python.exe" -m streamlit run "app.py" --server.headless=false --server.address=127.0.0.1 --server.port=8501 --browser.gatherUsageStats=false
echo.
echo Dashboard stopped. Press any key to close.
pause >nul
