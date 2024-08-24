from sqlalchemy.orm import Relationship

from app.sql_alchemy.database import Base
from sqlalchemy import Column, String, UUID, Boolean, text, DateTime, ForeignKey


# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship


class Posts(Base):
    __tablename__ = "posts"
    uid = Column(name='uid', type_=UUID, server_default=text('gen_random_uuid()'), primary_key=True, nullable=False, )
    title = Column(name='post_title', type_=String, nullable=False)
    content = Column(name='post_content', type_=String, nullable=False)
    is_published = Column(name='is_published', type_=Boolean, server_default='True')
    created_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'))
    user_uid = Column(ForeignKey("users.uid", ondelete="CASCADE"), name='user_uid', type_=UUID, nullable=False, )
    user_info = Relationship('Users')

class Users(Base):
    __tablename__ = 'users'
    uid = Column(name='uid', type_=UUID, server_default=text('gen_random_uuid()'), primary_key=True, nullable=False)
    first_name = Column(name='first_name', type_=String, nullable=False)
    last_name = Column(name='last_name', type_=String, nullable=False)
    email_id = Column(name='email', type_=String, nullable=False, unique=True)
    password = Column(name='password', type_=String, nullable=False)
    created_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'), nullable=False)