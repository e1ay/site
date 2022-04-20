import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Delivery(SqlAlchemyBase):
    __tablename__ = 'delivery'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    method = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    get_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    give_date = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)