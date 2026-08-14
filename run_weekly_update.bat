@echo off
chcp 65001 >nul
echo ========================================
echo   AI Research Tracker - 每周论文更新
echo   仅暂存到「每周增量更新」模块
echo   归档需手动选择
echo ========================================
echo.

cd /d D:\ai_research
call .venv\Scripts\activate.bat

python weekly_update.py

echo.
echo ========================================
echo   阶段一完成，候选数据已保存
echo   阶段二由 Agent（麦芽）评估并写入
echo   weekly-update/ 子页面
echo.
echo   主人查看后，可对我说：
echo   "把第X篇归档到LLM论文库"
echo ========================================
pause
