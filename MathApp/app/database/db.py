from sqlalchemy import MetaData, create_engine
from databases import Database
from config.settings import settings


metadata = MetaData()


engine = create_engine(
    settings.database_url.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False}
)


database = Database(settings.database_url)
