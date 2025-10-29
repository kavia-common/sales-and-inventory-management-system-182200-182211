@ECHO OFF
REM Simplified Gradle wrapper for CI placeholder at repo root.
IF EXIST "%~dp0\gradle\wrapper\gradle-wrapper.properties" (
  WHERE gradle >NUL 2>&1
  IF %ERRORLEVEL% EQU 0 (
    gradle %*
    EXIT /B 0
  ) ELSE (
    ECHO Gradle CLI not installed in CI container. Skipping.
    EXIT /B 0
  )
) ELSE (
  ECHO No gradle/wrapper properties found at repo root. Skipping.
  EXIT /B 0
)
