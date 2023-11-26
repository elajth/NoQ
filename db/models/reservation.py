from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from ..db_setup import Base
from .user import User
from .mixins import Timestamp

class Reservation(Timestamp, Base):
    __tablename__= "reservations"

    id = Column(Integer, primary_key=True, index=True)
    start_date_time = Column(DateTime, nullable=False)
    end_date_time = Column(DateTime, nullable=False)
    reached_limit = Column(Boolean, nullable=False)
    casemanager_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id") , nullable=False)