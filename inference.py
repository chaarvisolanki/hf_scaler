import os
import json
from app.env import TaskSchedulerEnv
from app.models import Action


def schedule_by_deadline(tasks):
    """Sort tasks by deadline"""
    return sorted(tasks, key=lambda t: (t.deadline.hour, t.deadline.minute))


def schedule_by_importance(tasks):
    """Sort tasks by importance (higher first) then deadline"""
    return sorted(tasks, key=lambda t: (-t.importance, t.deadline.hour * 60 + t.deadline.minute))


def schedule_smart(tasks):
    """Smart scheduling: Urgent -> High importance -> Dependencies"""
    # Separate urgent tasks
    urgent = [t for t in tasks if t.category.value == "urgent"]
    others = [t for t in tasks if t.category.value != "urgent"]
    
    # Sort by importance
    sorted_tasks = sorted(others, key=lambda t: (-t.importance, t.deadline.hour * 60 + t.deadline.minute))
    
    # Put urgent tasks first
    return urgent + sorted_tasks


def run_inference(task_level: str) -> dict:
    """Run inference on a task level"""
    env = TaskSchedulerEnv(task_level=task_level)
    obs = env.reset()
    
    print(f"[START] Task: {task_level}")
    
    # Get available tasks
    tasks = obs.available_tasks
    
    # Apply scheduling heuristic based on difficulty
    if task_level == "easy":
        scheduled_order = schedule_by_deadline(tasks)
    elif task_level == "medium":
        scheduled_order = schedule_by_importance(tasks)
    else:
        scheduled_order = schedule_smart(tasks)
    
    # Get task IDs in order
    task_ids = [t.task_id for t in scheduled_order]
    
    print(f"[PLAN] Scheduled order: {task_ids}")
    
    # Execute scheduling actions
    for task_id in task_ids:
        action = Action(action_type="schedule", task_id=task_id)
        obs, reward, done, info = env.step(action)
        print(f"[STEP] Task: {task_level}, Action: schedule {task_id}, Reward: {reward.score:.3f}")
    
    # Final step
    final_obs, final_reward, final_done, final_info = env.step(
        Action(action_type="skip")
    )
    
    print(f"[END] Task: {task_level}, Final Score: {final_reward.score:.3f}")
    print(f"[BREAKDOWN] {final_reward.breakdown}")
    
    return {
        "task_level": task_level,
        "score": final_reward.score,
        "breakdown": final_reward.breakdown
    }


def main():
    """Run inference on all task levels"""
    results = []
    
    print("=" * 60)
    print("Task Priority Scheduler - Baseline Inference")
    print("=" * 60)
    
    for level in ["easy", "medium", "hard"]:
        print(f"\n{'='*50}")
        result = run_inference(level)
        results.append(result)
    
    # Summary
    print(f"\n{'='*50}")
    print("FINAL RESULTS:")
    print("-" * 30)
    for r in results:
        print(f"  {r['task_level'].upper():8} : {r['score']:.3f}")
    
    avg_score = sum(r['score'] for r in results) / len(results)
    print("-" * 30)
    print(f"  {'AVERAGE':8} : {avg_score:.3f}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    main()
