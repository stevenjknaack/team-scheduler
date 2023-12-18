""" 
This class defines the models for interacting with the 10stars database
in  ORM/CRUD using Flask-SQLAlchemy.

Call the below functions on db.session

Create 
    <create Model> Model(var1 = val1, var2 = val2, ...)

    .add(Model)

    <commit>

Read
    .get(Model, primary_key_value)

    .execute(db.select(multple columns).filter_by(conditions))

    .scalars(db.select(Model or single column).filter_by(conditions))

    <use .first() if you only expect one result>

Update
    <get a Model from the db>

    <update the Model object's attributes>

    <commit>

Delete
    <get a Model from the db>

    .delete(Model)

    <commit>

<Commit>
    db.session.commit()

Bulk / Multi Row INSERT, upsert, UPDATE and DELETE are also available
https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#bulk-multi-row-insert-upsert-update-and-delete

More Comprehensive Docs
https://docs.sqlalchemy.org/en/20/tutorial/orm_data_manipulation.html#

Querying:
https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html

:author: Steven Knaack
"""
# mypy: disable-error-code="assignment"
# TODO fix the above mypy error in a more useful way

from .availablity_block import AvailabilityBlock
from .event import Event
from .group import Group
from .membership import Membership
from .team import Team
from .user import User
