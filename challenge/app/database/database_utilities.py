from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base
import challenge.app.config as config

address = "mysql://{usr}:{psw}@{url}:{port}/{name}".format(
    usr=config.database_info.usr,
    psw=config.database_info.psw,
    url=config.database_info.url,
    port=config.database_info.port,
    name=config.database_info.name
)
engine = create_engine(address)

Base = declarative_base()
Base.metadata.reflect(engine)


class LogPredictions(Base):
    __table__ = Base.metadata.tables["log_predictions"]


class LogSimilarities(Base):
    __table__ = Base.metadata.tables["log_similarities"]


def create_element(table, content, id_name="id"):
    element = table(**content)
    with Session(engine) as session:
        session.add(element)
        session.commit()
        session.refresh(element)

    return False if not id_name else element.__dict__[id_name]





