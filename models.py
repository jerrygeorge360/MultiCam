from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, LargeBinary
from typing import List
from flask_login import UserMixin


class Base(DeclarativeBase):
    ...


db = SQLAlchemy(model_class=Base)


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    token_data: Mapped[str] = mapped_column()
    profile_image_url: Mapped[str] = mapped_column()
    # streams: Mapped[List['Stream']] = relationship('Stream', back_populates='user')


# TODO : rewrite this User class to implement user mixin methods

# class Stream(db.Model):
#     object_id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
#     cam_angle: Mapped[str] = mapped_column()
#     cam_label: Mapped[str] = mapped_column()
#     stream_name: Mapped[str] = mapped_column()
#     stream_id: Mapped[str] = mapped_column()
#     password: Mapped[str] = mapped_column()
#     user_name: Mapped[str] = mapped_column()
#     embed_code: Mapped[str] = mapped_column()
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#     active: Mapped[bool] = mapped_column(default=False)
#     user: Mapped[User] = relationship('User', back_populates='streams')
