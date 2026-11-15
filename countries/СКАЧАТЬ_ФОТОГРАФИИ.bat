@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py download_photos.py
) else (
  python download_photos.py
)
echo.
echo Download finished or stopped. Read README_ru.txt if there were errors.
pause
