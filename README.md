Create migration:
    - alembic revision --autogenerate -m "Added account table"

Run:
- uvicorn main:app --reload