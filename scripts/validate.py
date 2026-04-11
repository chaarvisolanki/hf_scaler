<<<<<<< HEAD
# scripts/validate.py
#!/usr/bin/env python
"""Pre-submission validation script"""
import sys
import os
import subprocess
import requests
from app.env import TaskSchedulerEnv
from app.models import Action

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_env():
    """Validate environment implementation"""
    print("Validating Environment...")
    
    for level in ["easy", "medium", "hard"]:
        env = TaskSchedulerEnv(task_level=level)
        obs = env.reset()
        
        # Test step
        action = Action(action_type="schedule", task_id=obs.available_tasks[0].task_id)
        obs, reward, done, info = env.step(action)
        
        assert 0.0 <= reward.score <= 1.0, f"Invalid reward score: {reward.score}"
        
        # Test state
        state = env.state()
        assert state is not None
    
    print("✓ Environment validation passed")
    return True


def validate_docker():
    """Validate Dockerfile builds"""
    print("Validating Dockerfile...")
    
    result = subprocess.run(
        ["docker", "build", "-t", "hf-scaler-test", "."],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"✗ Docker build failed: {result.stderr}")
        return False
    
    print("✓ Dockerfile builds successfully")
    return True


def validate_space():
    """Validate HF Space responds"""
    print("Validating HF Space...")
    
    # Check if running locally
    try:
        resp = requests.get("http://localhost:7860/", timeout=5)
        if resp.status_code == 200:
            print("✓ HF Space responds correctly")
            return True
    except:
        pass
    
    print("⚠ HF Space not running locally (skipping)")
    return True


def main():
    print("Running Pre-submission Validation...\n")
    
    all_passed = True
    all_passed &= validate_env()
    all_passed &= validate_docker()
    all_passed &= validate_space()
    
    if all_passed:
        print("\n✓ All validations passed!")
        return 0
    else:
        print("\n✗ Some validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

=======
# scripts/validate.py
#!/usr/bin/env python
"""Pre-submission validation script"""
import sys
import os
import subprocess
import requests
from app.env import TaskSchedulerEnv
from app.models import Action

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def validate_env():
    """Validate environment implementation"""
    print("Validating Environment...")
    
    for level in ["easy", "medium", "hard"]:
        env = TaskSchedulerEnv(task_level=level)
        obs = env.reset()
        
        # Test step
        action = Action(action_type="schedule", task_id=obs.available_tasks[0].task_id)
        obs, reward, done, info = env.step(action)
        
        assert 0.0 <= reward.score <= 1.0, f"Invalid reward score: {reward.score}"
        
        # Test state
        state = env.state()
        assert state is not None
    
    print("✓ Environment validation passed")
    return True


def validate_docker():
    """Validate Dockerfile builds"""
    print("Validating Dockerfile...")
    
    result = subprocess.run(
        ["docker", "build", "-t", "hf-scaler-test", "."],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"✗ Docker build failed: {result.stderr}")
        return False
    
    print("✓ Dockerfile builds successfully")
    return True


def validate_space():
    """Validate HF Space responds"""
    print("Validating HF Space...")
    
    # Check if running locally
    try:
        resp = requests.get("http://localhost:7860/", timeout=5)
        if resp.status_code == 200:
            print("✓ HF Space responds correctly")
            return True
    except:
        pass
    
    print("⚠ HF Space not running locally (skipping)")
    return True


def main():
    print("Running Pre-submission Validation...\n")
    
    all_passed = True
    all_passed &= validate_env()
    all_passed &= validate_docker()
    all_passed &= validate_space()
    
    if all_passed:
        print("\n✓ All validations passed!")
        return 0
    else:
        print("\n✗ Some validations failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

>>>>>>> 9e48d59df39c9a052039194c2cde127befed3b61
