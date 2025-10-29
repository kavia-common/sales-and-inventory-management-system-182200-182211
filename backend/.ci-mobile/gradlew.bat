@echo off
REM CI mobile gradle wrapper shim. Some pipelines run from .ci-mobile directory.
echo [.ci-mobile] Gradle wrapper shim: no Android project present. Skipping.
exit /B 0
