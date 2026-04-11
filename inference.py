import os
from openai import OpenAI
from app.env import TaskSchedulerEnv
from app.models import Action

# 1. Configuration (Mandatory Defaults)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8B")

# 2. HF_TOKEN (No Default allowed)
HF_TOKEN = os.getenv("HF_TOKEN")


def run_inference():
    # 3. OpenAI Client Integration
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN
    )

    print("[START]")

    results = []
    for task_level in ["easy", "medium", "hard"]:
        print(f"[STEP] Starting task level: {task_level}")

        # Initialize environment
        env = TaskSchedulerEnv(task_level=task_level)
        obs = env.reset()

        # Get available tasks
        tasks = obs.available_tasks
        task_info = "\n".join([
            f"- {t.task_id}: {t.title} (deadline={t.deadline.isoformat()}, importance={t.importance}, dependencies={t.dependencies})"
            for t in tasks
        ])

        # Build prompt for LLM
        prompt = (
            f"You are a task scheduler. Given the following tasks for level '{task_level}', "
            f"schedule them in optimal order considering deadlines, importance, and dependencies.\n\n"
            f"Tasks:\n{task_info}\n\n"
            f"Respond with a JSON list of task_ids in the order they should be scheduled, "
            f"e.g., [\"t2\", \"t1\", \"t3\"]"
        )

        # 4. LLM Call
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        llm_response = response.choices[0].message.content
        print(f"[STEP] LLM Response: {llm_response}")

        # Parse LLM response and execute actions
        try:
            import json
            import re
            # Extract JSON list from response
            match = re.search(r'\[.*\]', llm_response)
            if match:
                scheduled_order = json.loads(match.group())
            else:
                scheduled_order = [t.task_id for t in tasks]
        except Exception:
            scheduled_order = [t.task_id for t in tasks]

        # Execute scheduling
        for task_id in scheduled_order:
            action = Action(action_type="schedule", task_id=task_id)
            obs, reward, done, info = env.step(action)
            print(f"[STEP] Scheduled task: {task_id}, Reward: {reward.score:.3f}")

        # Final step
        final_obs, final_reward, final_done, final_info = env.step(
            Action(action_type="skip")
        )

        results.append({
            "task_level": task_level,
            "score": final_reward.score,
            "breakdown": final_reward.breakdown
        })
        print(f"[STEP] Completed level: {task_level}, Final Score: {final_reward.score:.3f}")

    print("[END]")


if __name__ == "__main__":
    run_inference()
