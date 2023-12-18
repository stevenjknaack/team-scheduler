from ..extensions import db
from sqlalchemy.orm import relationship, Mapped
from ..models import *
from typing import List, Optional

class Group(db.Model) :
    """ Model of the `group` table. """
    __table__ = db.Model.metadata.tables['group']

    # define column properties
    id: Mapped[int] = __table__.columns['id']
    name: Mapped[str] = __table__.columns['name']
    description: Mapped[Optional[str]] =\
          __table__.columns['description']

    # define relationship properties
    teams: Mapped[List['Team']] =\
        relationship('Team', back_populates='group')
    events: Mapped[List['Event']] =\
        relationship('Event', back_populates='group')
    memberships: Mapped[List['Membership']] =\
        relationship('Membership', back_populates='group')
 
    # methods
    def get_group_level_events(self) -> List['Event'] :
        """ Returns a List of just the group-level events """
        group_level_events: List['Event'] = []

        for event in self.events :
            # filter out group level events
            if event.team_id is None :
                group_level_events.append(event)

        return group_level_events
    
    def __init__(self, name: str = 'Unnamed Group', 
                 description: str = 'No description provided') -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str :
        return f'Group(id: {self.id}; name: {self.name})'