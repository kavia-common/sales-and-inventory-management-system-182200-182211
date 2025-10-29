Always run CI from the repository root.
If your CI fails with './gradlew: No such file or directory', call one of these from repo root:
- bash .ci/bootstrap.sh
- bash run_mobile_ci_bootstrap.sh
- bash .ci/init.sh && ./gradlew :mobile_frontend_app:test
