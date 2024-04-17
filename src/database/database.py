from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# Database engine and session setup
engine = create_engine("sqlite:///sessions.sqlite3")
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for declarative models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import src.database.models

    Base.metadata.create_all(bind=engine, checkfirst=True)
