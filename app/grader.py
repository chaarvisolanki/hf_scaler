from datetime import time
from typing import Tuple
from app.models import Observation


def calculate_score(observation: Observation, task_level: str) -> Tuple[float, dict]:
    """Calculate reward score based on task scheduling quality"""
    
    scheduled = observation.scheduled_tasks
    
    if not scheduled:
        return 0.0, {"error": "No tasks scheduled"}
    
    scheduled_ids = [t.task_id for t in scheduled]
    
    # 1. Deadline compliance
    on_time_count = 0
    for i, task in enumerate(scheduled):
        scheduled_minutes = 9 * 60 + i * 30
        deadline_minutes = task.deadline.hour * 60 + task.deadline.minute
        if scheduled_minutes < deadline_minutes:
            on_time_count += 1
    
    deadline_score = on_time_count / len(scheduled)
    
    # 2. Importance ordering
    importance_correct = sum(
        1 for i in range(len(scheduled) - 1)
        if scheduled[i].importance >= scheduled[i + 1].importance
    )
    importance_score = importance_correct / (len(scheduled) - 1) if len(scheduled) > 1 else 1.0
    
    # 3. Dependency satisfaction
    satisfied = 0
    total_deps = 0
    for task in scheduled:
        for dep in task.dependencies:
            total_deps += 1
            if dep in scheduled_ids:
                if scheduled_ids.index(dep) < scheduled_ids.index(task.task_id):
                    satisfied += 1
    
    dependency_score = satisfied / total_deps if total_deps > 0 else 1.0
    
    # 4. Feasibility
    total_duration = sum(t.estimated_duration for t in scheduled)
    feasibility_score = min(total_duration / (8 * 60), 1.0)
    
    # Weighted total
    if task_level == "easy":
        total_score = deadline_score * 0.7 + importance_score * 0.3
    elif task_level == "medium":
        total_score = deadline_score * 0.4 + importance_score * 0.3 + dependency_score * 0.3
    else:
        total_score = deadline_score * 0.3 + importance_score * 0.25 + dependency_score * 0.25 + feasibility_score * 0.2
    
    breakdown = {
        "deadline_compliance": round(deadline_score, 3),
        "importance_ordering": round(importance_score, 3),
        "dependency_satisfaction": round(dependency_score, 3),
        "time_feasibility": round(feasibility_score, 3),
        "total": round(min(total_score, 1.0), 3)
    }
    
    return min(total_score, 1.0), breakdown
