@echo off
REM ============================================================
REM  deploy_local.bat  —  Lokal dev uchun migrate + seed
REM  Ishlatish:
REM    deploy_local.bat            (migrate + seed)
REM    deploy_local.bat --no-seed  (faqat migrate)
REM    deploy_local.bat --clear    (migrate + tozalab seed)
REM ============================================================

set SETTINGS=config.settings.dev
set RUN_SEED=1
set CLEAR_FLAG=

:parse_args
if "%1"=="--no-seed" ( set RUN_SEED=0 & shift & goto parse_args )
if "%1"=="--clear"   ( set CLEAR_FLAG=--clear & shift & goto parse_args )

echo.
echo ============================================
echo   O'ZDSA LOCAL DEPLOY — settings: %SETTINGS%
echo ============================================

echo.
echo [1/3] migrate...
python manage.py migrate --settings=%SETTINGS%
if errorlevel 1 ( echo [XATO] migrate muvaffaqiyatsiz! & exit /b 1 )

echo.
echo [2/3] collectstatic...
python manage.py collectstatic --noinput --settings=%SETTINGS%

if "%RUN_SEED%"=="1" (
  echo.
  echo [3/3] seed_all %CLEAR_FLAG% ...
  python manage.py seed_all %CLEAR_FLAG% --settings=%SETTINGS%
  if errorlevel 1 ( echo [XATO] seed_all muvaffaqiyatsiz! & exit /b 1 )
) else (
  echo.
  echo [3/3] seed o'tkazib yuborildi.
)

echo.
echo ============================================
echo   DEPLOY MUVAFFAQIYATLI YAKUNLANDI
echo ============================================
echo.
