from src.database.config import Session
from alembic_migrations.metadatas import metadatas
from src.database.model import tables


def truncate_database() -> None:
    for table in tables:
        table_name = table.__tablename__
        Session.execute(f"TRUNCATE {table_name} restart identity CASCADE")
        Session.commit()
