from app.sql_alchemy.database import Base
from sqlalchemy import Column, String, UUID, Boolean, text, DateTime

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
    create_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'))
