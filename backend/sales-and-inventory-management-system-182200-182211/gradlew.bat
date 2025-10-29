@echo off
REM Backend container root gradlew shim forwarding to repository root.
setlocal
set ROOT=%~dp0..
if exist "%ROOT%\gradlew.bat" (
  call "%ROOT%\gradlew.bat" %*
  exit /b %errorlevel%
)
if exist "%ROOT%\gradlew" (
  bash "%ROOT%\gradlew" %*
  exit /b %errorlevel%
)
echo [backend workspace] Root gradlew shim not found; no-op. 1>&2
exit /b 0
endlocal
