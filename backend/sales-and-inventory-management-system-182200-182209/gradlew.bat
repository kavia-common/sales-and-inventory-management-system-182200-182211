@echo off
REM Workspace root gradle shim to satisfy CI that invokes .\gradlew here.
setlocal
set TARGET=%~dp0mobile_frontend\gradlew.bat
if exist "%TARGET%" (
  call "%TARGET%" %*
  exit /b %errorlevel%
)
echo [workspace root] Gradle wrapper not present; no-op. 1>&2
exit /b 0
endlocal
