Contributing

Backend (FastAPI):
- Install deps: pip install -r sales-and-inventory-management-system-182200-182211/backend/requirements.txt
- Run: cd sales-and-inventory-management-system-182200-182211/backend && bash run_server.sh
- DB env: see backend/.env.example and backend/ENV_VARS.md

Mobile (Android):
- Without wrapper: bash sales-and-inventory-management-system-182200-182209/run_mobile_no_wrapper.sh :app:test
- Bootstrap: bash run_mobile_ci_bootstrap.sh
- If CI insists on ./gradlew, run from repo root and execute:
  - bash .ci/init.sh && ./gradlew :mobile_frontend_app:test

CI Helpers:
- bash CI_ENTRYPOINT.sh
- bash ensure_gradlew_and_run.sh
- bash create_temp_gradle_wrapper_and_test.sh
