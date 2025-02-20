from sqlalchemy import Column, String, UUID, Boolean, text, DateTime, ForeignKey, JSON, BLOB
from sqlalchemy.orm import Relationship

from app.sql_alchemy.database import Base


class Users(Base):
    __tablename__ = 'users'
    uid = Column(name='uid', type_=UUID, server_default=text('gen_random_uuid()'), primary_key=True, nullable=False)
    first_name = Column(name='first_name', type_=String, nullable=False)
    last_name = Column(name='last_name', type_=String, nullable=False)
    designation = Column(name='designation', type_=String, nullable=False)
    email_id = Column(name='email', type_=String, nullable=False, unique=True)
    password = Column(name='password', type_=String, nullable=False)
    created_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'), nullable=False)

class KnownDiffs(Base):
    __tablename__ = 'known_diffs'
    uid = Column(name='uid', type_=UUID, server_default=text('gen_random_uuid()'), primary_key=True, nullable=False)
    diff_name = Column(name='diff_name', type_=String, nullable=False)
    rule_id = Column(name='rule_id', type_=String, nullable=False)
    diff_url = Column(name='diff_url', type_=String, nullable=False)
    description = Column(name='description', type_=JSON, nullable=False)
    raised_by = Column(name='raised_by', type_=String, nullable=False, unique=True)
    diff_image = Column(name='diff_image', type_=BLOB, nullable=False, unique=True)
    assigned_to = Column(name='assigned_to', type_=String, nullable=False)
    is_active = Column(name='is_active', type_=Boolean, server_default='True')
    created_on = Column(name='created_at', type_=DateTime(timezone=True), server_default=text('Now()'), nullable=False)

