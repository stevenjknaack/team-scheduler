from ..extensions import db
from sqlalchemy.orm import relationship, Mapped
from ..models import *
from .channels import user_event_channel, user_team_channel
from typing import List

class User(db.Model) :
    """ Model of the `user` table. """
    __table__ = db.Model.metadata.tables['user']

    # define column properties
    email: Mapped[str] = __table__.columns['email']
    username: Mapped[str] = __table__.columns['username']
    password: Mapped[str] = __table__.columns['password']

    # define relationship properties
    availability_blocks: Mapped[List['AvailabilityBlock']] =\
        relationship('AvailabilityBlock', back_populates='user')
    memberships: Mapped[List['Membership']] =\
        relationship('Membership', back_populates='user')
    teams: Mapped[List['Team']] =\
        relationship('Team', secondary=user_team_channel, back_populates='members')
    events: Mapped[List['Event']] =\
        relationship('Event', secondary=user_event_channel, back_populates='participants')

    # methods
    def __init__(self, email: str, username: str, password: str) -> None :
        self.email = email
        self.username = username
        self.password = password
    
    def __repr__(self) -> str :
        return f'User(name: {self.username}; email: {self.email})'
    
    def get_group_invites(self) -> List['Group'] :
        """:returns: list of groups that are inviting the user"""
        group_invites: List['Group'] = []
        for membership in self.memberships :
            if membership.role == 'invitee' :
                group_invites.append(membership.group)
        return group_invites