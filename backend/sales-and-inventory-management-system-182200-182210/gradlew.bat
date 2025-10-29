@ECHO OFF
REM Database workspace stub for CI calling gradlew.bat from this directory.
SETLOCAL ENABLEDELAYEDEXPANSION

SET HERE=%~dp0
SET ROOT=%HERE%..

IF EXIST "%ROOT%\gradlew.bat" (
  CALL "%ROOT%\gradlew.bat" %*
  EXIT /B %ERRORLEVEL%
)

WHERE gradle >NUL 2>&1
IF %ERRORLEVEL%==0 (
  gradle %*
  EXIT /B %ERRORLEVEL%
)

ECHO Database workspace: Gradle wrapper not found and system 'gradle' not installed. No-op. 1>&2
EXIT /B 0
