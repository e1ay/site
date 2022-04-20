import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Foods(SqlAlchemyBase):
    __tablename__ = 'foods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    desc = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    pic = sqlalchemy.Column(sqlalchemy.String, nullable=False)
