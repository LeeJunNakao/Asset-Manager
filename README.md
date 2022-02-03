Create migration:
    - alembic revision --autogenerate -m "Added account table"
Migrate
    - alembic upgrade head

Run:
- uvicorn main:app --reload

Docker: 
- docker build -t asset-manager-backend .
- docker run -d -p 8000:80 asset-manager-backend