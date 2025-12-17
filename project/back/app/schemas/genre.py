from pydantic import BaseModel, ConfigDict
from typing import Optional

model_cfg = ConfigDict(from_attributes=True)

class GenreBase(BaseModel):
    model_config = model_cfg

    id: int
    name: str


class GenreDetail(GenreBase):
    description: Optional[str] = None
