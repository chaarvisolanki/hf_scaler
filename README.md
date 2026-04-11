---
title: hf_scaler
emoji: 📅
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "3.11"
app_file: app.py
pinned: false
---

# Task Priority Scheduler

A real-world OpenEnv environment for AI agents to learn task scheduling and prioritization.

## Overview

This environment simulates a daily task scheduling scenario where an AI agent must prioritize and schedule tasks based on:
- Deadline
- Importance level (1-5)
- Dependencies between tasks
- Estimated duration

## Task Levels

| Level | Description | Tasks | Difficulty | Expected Score |
|-------|-------------|-------|------------|----------------|
| Easy | Sort by deadline only | 3 | Easy | 0.8-1.0 |
| Medium | Deadline + importance + dependencies | 5 | Medium | 0.6-0.8 |
| Hard | Full optimization with all constraints | 8 | Hard | 0.4-0.7 |

## Observation Space

- `current_time`: Current time (HH:MM format)
- `available_tasks`: List of unscheduled tasks
- `scheduled_tasks`: List of tasks already scheduled
- `day_start`: Workday start (default: 9:00)
- `day_end`: Workday end (default: 17:00)

## Action Space

| Action | Parameters | Description |
|--------|------------|-------------|
| schedule | task_id | Schedule a task |
| reorder | new_order | Reorder scheduled tasks |
| skip | - | Skip current step |

## Reward Function

Weighted scoring based on:
- Deadline compliance (30-70%)
- Importance ordering (25-30%)
- Dependency satisfaction (25-30%)
- Time feasibility (20%)

## Baseline Scores

| Task Level | Score |
|------------|-------|
| Easy | 1.000 |
| Medium | 1.000 |
| Hard | 0.879 |
| **Average** | **0.960** |

## Setup

```bash
pip install -r requirements.txt
