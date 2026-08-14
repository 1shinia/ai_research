@echo off
chcp 65001 >nul
echo ========================================
echo   AI Research Tracker Wiki
echo ========================================
echo.

:: 检查是否已有服务在运行
netstat -ano 2>nul | findstr ":8000.*LISTEN" >nul
if not errorlevel 1 (
    echo [✓] 服务已在运行中
    goto OPEN_CHROME
)

:: 使用 wmic 创建独立进程（不会被父进程终止）
echo 正在启动 MkDocs 服务...
wmic process call create "D:\ai_research\.venv\Scripts\mkdocs.exe serve -f D:\ai_research\mkdocs.yml --dev-addr 127.0.0.1:8000" 2>nul | findstr "ProcessId" >nul
if errorlevel 1 (
    echo [✗] 启动失败
    pause
    exit /b 1
)

echo 等待服务初始化...
timeout /t 5 /nobreak >nul

:OPEN_CHROME
echo 正在用谷歌浏览器打开 http://127.0.0.1:8000 ...
start "" "C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chrome.exe" http://127.0.0.1:8000

echo.
echo [✓] 服务已启动！可在 Chrome 中访问 http://127.0.0.1:8000
echo.
