import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger("autoblur.db")


from configs.settings import settings
DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
logger.debug(f"Using DATABASE_URL: {DATABASE_URL}")

try:
	engine = create_engine(DATABASE_URL)
	logger.info("SQLAlchemy engine created.")
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	logger.info("SessionLocal configured.")
except Exception as e:
	logger.error(f"Database initialization error: {e}", exc_info=True)
