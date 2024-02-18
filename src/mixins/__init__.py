from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class MixinTimestamps():
  created_at: Mapped[datetime] = mapped_column(default = lambda: datetime.utcnow())
  updated_at: Mapped[datetime] = mapped_column(default = lambda: datetime.utcnow(),
                                               onupdate = lambda: datetime.utcnow())
