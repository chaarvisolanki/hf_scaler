from datetime import time
from typing import List, Tuple
from app.models import Observation, Action, Reward, Task
from app.tasks import TASKS
from app.grader import calculate_score


class TaskSchedulerEnv:
    """OpenEnv-compatible Task Scheduler Environment"""
    
    def __init__(self, task_level: str = "easy"):
        self.task_level = task_level
        self.current_time = time(9, 0)
        self.available_tasks: List[Task] = []
        self.scheduled_tasks: List[Task] = []
        self.day_start = time(9, 0)
        self.day_end = time(17, 0)
        self.max_steps = 10
        self.current_step = 0
        self.done = False
        
    def reset(self) -> Observation:
        self.current_time = time(9, 0)
        self.scheduled_tasks = []
        self.current_step = 0
        self.done = False
        task_getter = TASKS.get(self.task_level, TASKS["easy"])
        self.available_tasks = task_getter()
        return Observation(
            current_time=self.current_time,
            available_tasks=self.available_tasks,
            scheduled_tasks=self.scheduled_tasks,
            day_start=self.day_start,
            day_end=self.day_end
        )
    
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        self.current_step += 1
        
        if action.action_type == "schedule":
            task = next(
                (t for t in self.available_tasks if t.task_id == action.task_id),
                None
            )
            if task and task not in self.scheduled_tasks:
                self.scheduled_tasks.append(task)
        
        elif action.action_type == "reorder":
            if action.new_order:
                task_map = {t.task_id: t for t in self.scheduled_tasks}
                self.scheduled_tasks = [
                    task_map[tid] for tid in action.new_order
                    if tid in task_map
                ]
        
        self.done = self.current_step >= self.max_steps or len(self.available_tasks) == 0
        
        obs = self.state()
        score, breakdown = calculate_score(obs, self.task_level)
        reward = Reward(score=score, breakdown=breakdown)
        
        return obs, reward, self.done, {"step": self.current_step, "task_level": self.task_level}
    
    def state(self) -> Observation:
        return Observation(
            current_time=self.current_time,
            available_tasks=self.available_tasks,
            scheduled_tasks=self.scheduled_tasks,
            day_start=self.day_start,
            day_end=self.day_end
        )
