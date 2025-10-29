Migrations

Current approach:
- Tables are auto-created via SQLAlchemy Base.metadata.create_all on startup.

Future (recommended):
- Integrate Alembic for schema migrations.
- Typical commands:
  - alembic init migrations
  - alembic revision --autogenerate -m "init"
  - alembic upgrade head
