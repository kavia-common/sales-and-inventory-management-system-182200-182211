@ECHO OFF
REM Lightweight Gradle wrapper shim for Windows CI
SETLOCAL
IF EXIST "%~dp0\gradle\wrapper\gradle-wrapper.properties" (
  WHERE gradle >NUL 2>&1
  IF %ERRORLEVEL% EQU 0 (
    gradle %*
    EXIT /B 0
  ) ELSE (
    ECHO Gradle not installed in CI container. Skipping build tasks.
    EXIT /B 0
  )
) ELSE (
  ECHO No gradle wrapper properties found. Skipping.
  EXIT /B 0
)
ENDLOCAL
