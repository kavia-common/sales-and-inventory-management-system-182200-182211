This directory includes multiple Gradle shims to satisfy CI:
- gradlew (POSIX shim)
- gradlew.bat (Windows shim)
- gradlew.stub (helper)
- check.sh (bootstrap)
- run-check.sh (fallback creator)

If CI still cannot find ./gradlew, adjust the job to run:
  bash check.sh
or
  bash run-check.sh
