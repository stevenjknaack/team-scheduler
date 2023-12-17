from ..extensions import db
from sqlalchemy.orm import relationship, Mapped
from ..models import *

class Membership(db.Model) :
    """ 
    Association object modeling many-to-many relationship between
    User and Group with the added context of Membership.role, provided
    by the `in_group` table.
    """
    __table__ = db.Model.metadata.tables['in_group']

    # define column properties
    user_email: Mapped[str] = __table__.columns['user_email']
    group_id: Mapped[int] = __table__.columns['group_id']
    role: Mapped[str] = __table__.columns['role']

    # define relationship properties
    user: Mapped['User'] =\
        relationship('User', back_populates='memberships')
    group: Mapped['Group'] =\
        relationship('Group', back_populates='memberships')

    # methods
    def __init__(self, user_email: str, group_id: int, role: str = 'invitee') -> None:
        """:role: must be in ['invitee', 'requester', 'participant', 'admin', 'owner'] """
        self.user_email = user_email
        self.group_id = group_id
        self.role = role

    def __repr__(self) -> str :
        return f'Membership(user_email: {self.user_email}; group_id: {self.group_id})>'