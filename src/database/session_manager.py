from contextlib import contextmanager
from src.database.database import db_session


@contextmanager
def get_db():
    try:
        yield db_session
    finally:
        db_session.remove()  # Properly close the session
