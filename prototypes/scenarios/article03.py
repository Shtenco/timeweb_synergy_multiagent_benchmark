"""Analytical coordination simulation, not an LLM-agent benchmark."""

from __future__ import annotations

import math


def run(seed: int = 42, independent_tasks: int = 15, total_work_budget: int = 15000) -> dict:
    if independent_tasks < 1 or total_work_budget < 1:
        raise ValueError("task count and work budget must be positive")
    rows = []
    for workers in (1, 3, 15):
        assigned = min(workers, independent_tasks)
        rows.append({
            "workers": workers,
            "work_budget": total_work_budget,
            "independent_tasks": independent_tasks,
            "parallel_rounds": math.ceil(independent_tasks / workers),
            "coordination_edges": workers * (workers - 1) // 2,
            "idle_workers_per_final_round": max(0, workers - (independent_tasks % workers or workers)),
            "assumption": "equal-duration independent tasks; no model calls are made",
            "workers_assigned_at_least_one_task": assigned,
        })
    return {
        "evidence_type": "simulation",
        "seed": seed,
        "results": rows,
        "limitations": [
            "This is an analytical scheduling toy, not a run of 1, 3, or 15 LLM agents.",
            "Real token usage, answer quality, latency, and coordination failures are not measured.",
        ],
    }
