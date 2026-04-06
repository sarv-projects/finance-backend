from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal, Optional

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0, description="The transaction amount must be positive")
    description: Optional[str] = Field(default=None, max_length=255)
    category: str = Field(min_length=1)
    type: Literal["income", "expense"]
    date: datetime = Field(default_factory=datetime.now)