@ECHO OFF
REM App module gradlew shim for Windows CI
SET DIR=%~dp0
cd "%DIR%\.."
bash "run_without_wrapper.sh" %*
