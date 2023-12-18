from ..extensions import db
from sqlalchemy.orm import relationship, Mapped
from .channels import user_event_channel
from ..models import *
from datetime import date, time
from typing import List, Optional

class Event(db.Model) :
    """ Model of the `Event` table. """
    __table__ = db.Model.metadata.tables['event']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
        __table__.columns['description']
    start_date: Mapped[date] = __table__.columns['start_date']
    end_date: Mapped[date] = __table__.columns['end_date']
    reg_start_day: Mapped[Optional[str]] =\
        __table__.columns['reg_start_day']
    reg_end_day: Mapped[Optional[str]] =\
        __table__.columns['reg_end_day']
    start_time: Mapped[time] = __table__.columns['start_time']
    end_time: Mapped[time] = __table__.columns['end_time']
    edit_permission: Mapped[str] = __table__.columns['edit_permission']
    group_id: Mapped[Optional[int]] = __table__.columns['group_id']
    team_id: Mapped[Optional[int]] = __table__.columns['team_id']

    # define relationship properties
    group: Mapped['Group'] =\
        relationship('Group', back_populates='events')
    team: Mapped['Team'] =\
        relationship('Team', back_populates='events')
    #TODO ENSURE TEAM AND GROUP DONT CONFLICT
    participants: Mapped[List['User']] =\
        relationship('User', secondary=user_event_channel, back_populates='events')
    
    # methods
    def is_recurring(self) -> bool :
        """ Returns true only if this event repeats weekly """
        return not self.reg_start_day and not self.reg_end_day

    def __init__(self, start_date: date, end_date: date, 
                 start_time: time, end_time: time, group_id: int,
                 team_id: Optional[int] = None, name: str = 'Unnamed Event',
                 description: Optional[str] = None, reg_start_day: Optional[str] = None,
                 reg_end_day: Optional[str] = None, edit_permission: str = 'group_admin') -> None :
        """ 
        :edit_permission: must be in ['member', 'group_admin']
        and if defined reg_start_day and reg_end_day must be in 
            ['sunday', 'monday', 'tuesday', 
            'wednesday', 'thursday', 'friday', 'saturday']
        """
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.reg_start_day = reg_start_day
        self.reg_end_day = reg_end_day
        self.start_time = start_time
        self.end_time = end_time
        self.edit_permission = edit_permission
        self.group_id = group_id
        self.team_id = team_id

    def __repr__(self) -> str :
        return f'Event(id: {self.id}; name: {self.name}; group: {self.group_id})'