from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Union

class Event(BaseModel):
    topic: str = Field(..., example="sensorA")
    event_id: str = Field(..., example="abc-123")
    timestamp: datetime
    source: str
    payload: Dict

class Stats(BaseModel):
    received: int
    unique_processed: int
    duplicate_dropped: int
    topics: List[str]
    uptime: str
