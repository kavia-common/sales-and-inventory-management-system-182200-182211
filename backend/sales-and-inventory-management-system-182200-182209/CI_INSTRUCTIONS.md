# CI Instructions for Mobile Frontend

To build or test the Android mobile frontend from the repository root, use:

# Preferred (uses wrapper bootstrap)
bash sales-and-inventory-management-system-182200-182209/run_mobile_ci.sh assembleDebug
bash sales-and-inventory-management-system-182200-182209/run_mobile_ci.sh test

# Fallback (no wrapper): downloads Gradle from distributionUrl and runs it directly
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh assembleDebug
bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh test

These scripts ensure the working directory is the mobile_frontend. The fallback avoids requiring ./gradlew in CI.
