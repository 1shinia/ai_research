cd /d D:\ai_research
start "" /B python -m mkdocs serve -f mkdocs.yml --dev-addr 127.0.0.1:8000
timeout /t 5 /nobreak >nul
curl -s -o NUL -w "%%{http_code}" http://127.0.0.1:8000/ 2>&1
