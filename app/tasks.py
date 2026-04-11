from datetime import time
from typing import List
from app.models import Task, TaskCategory


def get_easy_tasks() -> List[Task]:
    """Easy: 3 tasks - sort by deadline only"""
    return [
        Task(task_id="t1", title="Reply to emails", description="Check and reply to important emails", deadline=time(11, 0), importance=3, estimated_duration=30, category=TaskCategory.WORK),
        Task(task_id="t2", title="Team standup meeting", description="Daily standup with the team", deadline=time(9, 30), importance=4, estimated_duration=15, category=TaskCategory.WORK),
        Task(task_id="t3", title="Submit timesheet", description="Fill out weekly timesheet", deadline=time(17, 0), importance=2, estimated_duration=10, category=TaskCategory.ADMIN),
    ]


def get_medium_tasks() -> List[Task]:
    """Medium: 5 tasks - deadline + importance + dependencies"""
    return [
        Task(task_id="t1", title="Client presentation", description="Prepare slides for client meeting", deadline=time(14, 0), importance=5, estimated_duration=120, category=TaskCategory.WORK),
        Task(task_id="t2", title="Code review", description="Review PR #342", deadline=time(16, 0), importance=3, estimated_duration=45, category=TaskCategory.WORK, dependencies=["t3"]),
        Task(task_id="t3", title="Complete feature branch", description="Finish authentication feature", deadline=time(12, 0), importance=4, estimated_duration=60, category=TaskCategory.WORK),
        Task(task_id="t4", title="Lunch break", description="Take lunch break", deadline=time(13, 0), importance=1, estimated_duration=60, category=TaskCategory.PERSONAL),
        Task(task_id="t5", title="Submit expense report", description="Submit monthly expenses", deadline=time(17, 0), importance=2, estimated_duration=20, category=TaskCategory.ADMIN),
    ]


def get_hard_tasks() -> List[Task]:
    """Hard: 8 tasks - full optimization with all constraints"""
    return [
        Task(task_id="t1", title="Project kickoff", description="Initial planning meeting", deadline=time(10, 0), importance=5, estimated_duration=60, category=TaskCategory.WORK),
        Task(task_id="t2", title="Write requirements", description="Document requirements", deadline=time(12, 0), importance=4, estimated_duration=90, category=TaskCategory.WORK, dependencies=["t1"]),
        Task(task_id="t3", title="Design architecture", description="Create architecture diagram", deadline=time(15, 0), importance=4, estimated_duration=120, category=TaskCategory.WORK, dependencies=["t2"]),
        Task(task_id="t4", title="Team sync", description="Sync with dev team", deadline=time(11, 0), importance=3, estimated_duration=30, category=TaskCategory.WORK),
        Task(task_id="t5", title="Code implementation", description="Implement core features", deadline=time(16, 30), importance=5, estimated_duration=180, category=TaskCategory.WORK, dependencies=["t3"]),
        Task(task_id="t6", title="Bug fix", description="Fix critical production bug", deadline=time(13, 0), importance=5, estimated_duration=45, category=TaskCategory.URGENT),
        Task(task_id="t7", title="Coffee break", description="Take a short break", deadline=time(14, 0), importance=1, estimated_duration=15, category=TaskCategory.PERSONAL),
        Task(task_id="t8", title="Wrap-up", description="Document progress", deadline=time(17, 0), importance=2, estimated_duration=15, category=TaskCategory.ADMIN),
    ]


TASKS = {
    "easy": get_easy_tasks,
    "medium": get_medium_tasks,
    "hard": get_hard_tasks,
}
