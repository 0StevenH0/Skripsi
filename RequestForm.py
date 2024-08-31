from pydantic import BaseModel
from typing import Optional

class ModelRequest(BaseModel):
    search: Optional[str] = None
