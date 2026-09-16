from typing import Optional

from pydantic import BaseModel

class ActionsSchema(BaseModel):
    action_type: str
    custom_time_text: Optional[str] = None
    message: Optional[str] = None
    timestamp: str

