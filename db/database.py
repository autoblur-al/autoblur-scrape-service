import logging
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models.base import Base

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger("autoblur.db")


from configs.settings import settings
# Use URL.create() to properly handle special characters in password
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=int(settings.db_port),
    database=settings.db_name
)
logger.debug(f"Connecting to database: {settings.db_name} on {settings.db_host}:{settings.db_port} as {settings.db_user}")

try:
	engine = create_engine(DATABASE_URL)
	logger.info("SQLAlchemy engine created.")
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	logger.info("SessionLocal configured.")
except Exception as e:
	logger.error(f"Database initialization error: {e}", exc_info=True)
