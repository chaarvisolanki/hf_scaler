from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.env import TaskSchedulerEnv
from app.models import Action, Observation, Task, Reward

app = FastAPI(title="Task Priority Scheduler")

# Global environment instance
env: TaskSchedulerEnv = None


class ResetRequest(BaseModel):
    task_level: str = "easy"


class StepRequest(BaseModel):
    action: dict


def serialize_task(t: Task) -> dict:
    """Serialize a Task to JSON-compatible dict"""
    return {
        "task_id": t.task_id,
        "title": t.title,
        "description": t.description,
        "deadline": t.deadline.isoformat(),
        "importance": t.importance,
        "estimated_duration": t.estimated_duration,
        "dependencies": t.dependencies,
        "category": t.category.value,
        "completed": t.completed,
    }


def serialize_observation(obs: Observation) -> dict:
    """Serialize an Observation to JSON-compatible dict"""
    return {
        "current_time": obs.current_time.isoformat(),
        "available_tasks": [serialize_task(t) for t in obs.available_tasks],
        "scheduled_tasks": [serialize_task(t) for t in obs.scheduled_tasks],
        "day_start": obs.day_start.isoformat(),
        "day_end": obs.day_end.isoformat(),
    }


def serialize_reward(reward: Reward) -> dict:
    """Serialize a Reward to JSON-compatible dict"""
    return {
        "score": reward.score,
        "breakdown": reward.breakdown,
    }


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/reset")
async def reset(request: ResetRequest):
    global env
    env = TaskSchedulerEnv(task_level=request.task_level)
    obs = env.reset()
    return JSONResponse(content=serialize_observation(obs))


@app.post("/step")
async def step(request: StepRequest):
    if env is None:
        raise HTTPException(status_code=400, detail="Call /reset first")

    action = Action(**request.action)
    obs, reward, done, info = env.step(action)

    return JSONResponse(content={
        "observation": serialize_observation(obs),
        "reward": serialize_reward(reward),
        "done": done,
        "info": info
    })


@app.get("/state")
async def state():
    if env is None:
        raise HTTPException(status_code=400, detail="Call /reset first")
    return JSONResponse(content=serialize_observation(env.state()))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
