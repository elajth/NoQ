from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp

class User(Timestamp, Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    unokod = Column(String(100), nullable=False)
    reservation_uuid = Column(Integer, ForeignKey("reservations.id") , nullable=False)