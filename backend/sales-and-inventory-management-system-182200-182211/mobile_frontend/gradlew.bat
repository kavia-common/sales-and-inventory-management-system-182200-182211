@echo off
REM Backend workspace sibling 'mobile_frontend' shim for CI.
setlocal
set REPO_ROOT=%~dp0..\..
set TARGET=%REPO_ROOT%\sales-and-inventory-management-system-182200-182209\mobile_frontend\gradlew.bat
if exist "%TARGET%" (
  call "%TARGET%" %*
  exit /b %errorlevel%
)
echo [backend-sibling/mobile_frontend] No Android project detected. No-op. 1>&2
exit /b 0
endlocal
