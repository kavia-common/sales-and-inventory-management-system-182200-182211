Backend Docs Index

- README.md (features, run instructions, endpoints)
- ENV_VARS.md (environment variables)
- SECURITY_NOTES.md (security considerations)
- DIAGNOSTICS.md (diagnostic endpoints)
- ERROR_RESPONSES.md (error handling and codes)
- SCHEMAS.md (payload schemas summary)
- GST_AND_INVENTORY_RULES.md (business rules)

Utilities:
- run_server.sh (start dev server on port 3001)
- run_lint.sh (flake8 lint)
- run_tests.sh (pytest)
- EXPORT_OPENAPI.md / export_backend_openapi.sh (OpenAPI generation)
- RUN_AND_EXPORT.sh (quick server start + OpenAPI export)
- demo_e2e.sh (simple end-to-end cURL demo)

API:
- src/api/main.py (entry)
- src/api/register_routes.py (routers registration)
- src/api/register_products_paged.py (products paged route)
- src/api/error_handlers.py (global exception handler)
- src/api/info.py, routes_overview.py, root.py (utility endpoints)
- src/api/openapi_route.py (explicit OpenAPI route)
