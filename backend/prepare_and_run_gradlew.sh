#!/usr/bin/env sh
# Make shims executable and then run ./gradlew with passed args
set -eu
chmod +x ./gradlew || true
chmod +x ./gradlew.cmd || true
chmod +x ./gradlew-sh || true
chmod +x ./gradlew.shim || true
chmod +x ./gradle.sh || true
chmod +x .ci/init.sh || true
chmod +x run_mobile_ci_bootstrap.sh || true
chmod +x create_temp_gradle_wrapper_and_test.sh || true
# Now run the root gradle shim
./gradlew "$@"
