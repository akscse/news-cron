from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import List, Optional

class News(Document):
    preference_name: str
    heading: str
    description: str
    news_datetime: datetime  # ✅ renamed from datetime to avoid clash
    image: Optional[str] = None
    src: List[str] = Field(default_factory=list)
    inserted_at: datetime = Field(default_factory=datetime.utcnow)  # ✅ no ()

    class Settings:
        name = "news"
