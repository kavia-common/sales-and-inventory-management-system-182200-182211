@ECHO OFF
REM Root-level Gradle shim for Windows CI runners.
REM Delegates to the wrapper-less bootstrap runner.
SET SCRIPT_DIR=%~dp0
IF EXIST "%SCRIPT_DIR%.ci\init.sh" (
  bash "%SCRIPT_DIR%.ci\init.sh"
)
bash "%SCRIPT_DIR%run_mobile_ci_bootstrap.sh" %*
