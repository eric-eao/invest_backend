import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.routes.private_credit import categories

# banco de teste
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://investments_user:investments_pass@localhost:5432/investments_db_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    """
    Setup global para testes, garante tabelas antes de rodar a suíte inteira,
    e limpa ao final.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Session isolada por teste, com truncamento de tabelas
    e rollback para garantir consistência.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    session.execute(text("TRUNCATE TABLE private_credit_categories RESTART IDENTITY CASCADE;"))
    session.commit()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Injeção do banco de teste no app FastAPI para os testes.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides.clear()
    app.dependency_overrides[categories.get_db] = override_get_db

    print(">>>> usando banco de testes <<<<")

    return TestClient(app)
