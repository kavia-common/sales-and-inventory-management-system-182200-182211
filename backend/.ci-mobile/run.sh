#!/usr/bin/env bash
set -euo pipefail
echo "[.ci-mobile/run.sh] Bootstrapping gradle shims..."
bash ./bootstrap-mobile-ci.sh || true
bash ./ensure-gradle-shims.sh || true
echo "[.ci-mobile/run.sh] Trying ./gradlew --version ..."
./gradlew --version || true
echo "[.ci-mobile/run.sh] Trying relay script ..."
bash ./gradlew-relay.sh --version || true
echo "[.ci-mobile/run.sh] Done."
