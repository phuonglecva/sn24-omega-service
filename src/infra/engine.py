from sqlalchemy import create_engine

def create_sqlalchemy_engine(db_path: str = "sqlite:///db.sqlite"):
    return create_engine(db_path, echo=True)