from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import time


class TaskCategory(str, Enum):
    WORK = "work"
    PERSONAL = "personal"
    URGENT = "urgent"
    ADMIN = "admin"


class Task(BaseModel):
    task_id: str
    title: str
    description: str
    deadline: time
    importance: int = Field(ge=1, le=5)
    estimated_duration: int
    dependencies: List[str] = Field(default_factory=list)
    category: TaskCategory
    completed: bool = False


class Observation(BaseModel):
    current_time: time
    available_tasks: List[Task]
    scheduled_tasks: List[Task] = Field(default_factory=list)
    day_start: time = Field(default=time(9, 0))
    day_end: time = Field(default=time(17, 0))


class Action(BaseModel):
    action_type: str
    task_id: Optional[str] = None
    new_order: Optional[List[str]] = None


class Reward(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    breakdown: dict
