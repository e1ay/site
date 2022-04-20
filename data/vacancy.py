import sqlalchemy


from .db_session import SqlAlchemyBase


class Vacancy(SqlAlchemyBase):
    __tablename__ = 'vacancy'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    requirements = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    conditions = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    pay = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)


