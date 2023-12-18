from ..extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from ..models import *
from datetime import date, time

class AvailabilityBlock(db.Model) :
    """ Model of the `availability_block` table. """
    __table__ = db.Model.metadata.tables['availability_block']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    start_day: Mapped[str] = __table__.columns['start_day']
    end_day: Mapped[str] = __table__.columns['end_day']
    start_time: Mapped[time] = __table__.columns['start_time']
    end_time: Mapped[time] = __table__.columns['end_time']
    user_email: Mapped[str] = __table__.columns['user_email']

    # define relationship properties
    user: Mapped['User'] =\
        relationship('User', back_populates='availability_blocks')
    
    # methods
    def __init__(self, start_day: str, end_day: str, 
                 start_time: time, end_time: time, user_email: str) -> None :
        """ 
        start_day and end_day must be in 
            ['sunday', 'monday', 'tuesday', 
            'wednesday', 'thursday', 'friday', 'saturday']
        """
        self.start_day = start_day
        self.end_day = end_day
        self.start_time = start_time
        self.end_time = end_time
        self.user_email = user_email
    
    def __repr__(self) -> str :
        return f'AvailabilityBlock(id: {self.id})'