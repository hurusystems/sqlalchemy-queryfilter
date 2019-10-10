from sqlalchemy.orm import Session
import pytest
import app


@pytest.fixture(scope='session')
def engine():
    return app.db.engine


@pytest.yield_fixture(scope='session')
def tables(engine):
    app.db.metadata.create_all(engine)
    yield
    app.db.metadata.drop_all(engine)


@pytest.yield_fixture
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    session = Session(bind=connection)

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
