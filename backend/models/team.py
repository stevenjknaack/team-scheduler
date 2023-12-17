from ..extensions import db
from sqlalchemy.orm import relationship, Mapped
from .channels import user_team_channel
from ..models import *
from typing import List, Optional

class Team(db.Model) :
    """ Model of the `team` table. """
    __table__ = db.Model.metadata.tables['team']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
        __table__.columns['description']
    group_id: Mapped[int] = __table__.columns['group_id']

    # define relationship properties
    group: Mapped['Group'] =\
        relationship('Group', back_populates='teams')
    events: Mapped[List['Event']] =\
        relationship('Event', back_populates='team')
    members: Mapped[List['User']] =\
        relationship('User', secondary=user_team_channel, back_populates='teams')
    
    # methods
    def __init__(self, group_id: int, 
                 name: str = 'Unnamed Team', 
                 description: str = 'No description provided.') -> None :
        """
        id: steven
        """
        self.group_id = group_id
        self.name = name
        self.description = description
    
    def __repr__(self) -> str :
        return f'Team(id: {self.id}; name: {self.name})'