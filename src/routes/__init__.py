from src.db.alchemy import engine
from src.db.alchemy import SessionLocal
import psycopg2.extras

def get_db():
    '''
    does
    :return:
    '''
    db = SessionLocal()
    # logging.info("get_db")
    try:
        # logging.debug("yeilding db")
        yield db
    finally:
        # logging.debug("closing db")
        db.close()


def get_raw_db():
    '''
    does
    :return:
    '''
    db = engine.raw_connection()

    # logging.info("get_db")
    try:
        # logging.debug("yeilding db")
        yield db
    finally:
        # logging.debug("closing db")
        db.close()
