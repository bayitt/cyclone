from sqlalchemy.orm import relationship
from .setup import Base

class Application(Base):
    __tablename__ = "applications"