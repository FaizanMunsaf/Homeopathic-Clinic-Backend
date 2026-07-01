from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, String
from config.database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role = Column(String(255), nullable=True, default="super-admin", server_default="super-admin")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return str(self.username or self.email)  # Ensure readable name appears

    def __str__(self):
        return str(self.username or self.email)  # Works for UI display
