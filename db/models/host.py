from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Host(Timestamp, Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address1 = Column(String(100), nullable=False)
    address2 = Column(String(100), nullable=False)
    count_of_available_places = Column(Integer, nullable=False)
    total_available_places = Column(Integer, nullable=False)
