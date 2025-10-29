CI Hints:
- Do NOT call ./gradlew from repository root; use:
    bash ../../run_mobile_no_wrapper.sh :app:test
- Or from this directory:
    bash run_without_wrapper.sh :app:test
- If the build step insists on ./gradlew, ensure it changes directory to this folder first and runs:
    chmod +x gradlew && ./gradlew :app:test
