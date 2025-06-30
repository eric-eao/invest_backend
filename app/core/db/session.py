from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    raise RuntimeError("get_db não pode ser usado sem override")
