from datetime import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class TranslationDB(SqlAlchemyBase):
    __tablename__ = "translation"

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    queue = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relation("User")
    from_language = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    to_language = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    original_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translated_text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    added_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now)
