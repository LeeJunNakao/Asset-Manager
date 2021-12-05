Create migration:
    - alembic revision --autogenerate -m "Added account table"
Migrate
    - alembic upgrade head

Run:
- uvicorn main:app --reload