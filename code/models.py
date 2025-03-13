from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    date_of_birth = Column(Date)
    membership_type = Column(String)
    registration_date = Column(Date)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, index=True)  # Додано для унікальності та зручності пошуку

    @hybrid_property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @full_name.setter
    def full_name(self, full_name):
        parts = full_name.split()
        self.first_name = parts[0]
        self.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
