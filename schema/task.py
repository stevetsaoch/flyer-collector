# python
from datetime import datetime
from uuid import uuid4

# pydantic
from pydantic import BaseModel, Field

# enum
from enums.task import TaskStatus


class FlyerTask(BaseModel):
    type: str = Field(default="flyer")
    store_name: str
    start_time: datetime
    end_time: datetime
    publication_id: str
    pages: list | None = []


class ProductTask(BaseModel):
    type: str = Field(default="product")
    store_name: str
    publication_id: str
    url: str


class Task(BaseModel):
    uuid: str = Field(default=str(uuid4()))
    task: FlyerTask | ProductTask
    status: int = Field(default=TaskStatus.process.value)
    created_at: datetime = Field(default=datetime.now())
