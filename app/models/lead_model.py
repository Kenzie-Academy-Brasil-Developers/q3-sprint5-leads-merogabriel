from dataclasses import dataclass
from sqlalchemy import Column, Integer, DateTime, String
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Lead(db.Model):
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime)
    last_visit = Column(DateTime)
    visits = Column(Integer, default=1)


    @classmethod
    def check_json_types(cls, payload: dict):
        for value in payload.values():
            if type(value) != str:
                return False
        
        return True


    @classmethod
    def add_dates(cls, payload: dict):
        payload['creation_date'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        payload['last_visit'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        return payload


    def patch_visits(self):
        self.visits += 1
        self.last_visit = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        return self