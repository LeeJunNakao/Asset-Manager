# Instructions

## Development

### Database

- Create migration `alembic revision --autogenerate -m "Added account table"`
- Migrate: `alembic upgrade head`

### Server

- Run server: `uvicorn main:app --reload`

## Using Docker

- Build image: `docker build -t asset-manager-backend .`
- Running container: `docker run -d -p 8000:80 asset-manager-backend`
