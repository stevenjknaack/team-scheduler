from ..extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column

# table `in_team` relationship representation
user_team_channel = db.Model.metadata.tables['in_team']

# table `participates_in` relationship representation
user_event_channel = db.Model.metadata.tables['participates_in']