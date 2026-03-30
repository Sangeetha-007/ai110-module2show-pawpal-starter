# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling

1. mark_task_complete
2. warn_conflicts  
3. filter_tasks
4. sort_by_time

### Testing PawPal+

- To test PawPal+, run: python -m pytest

-This pytest tests: 
    - If tasks are returned in chronological order.
    - Confirms that marking a daily task complete creates a new task for the following day.
    - Verifies that the Scheduler flags duplicate times.

Confidence Level of tests: 4/5

### Features

  - Pet Profile Management — Store and display pet details (name, species, age, weight) with an attached health profile containing free-form notes. Owners can add or remove 
  pets; removing a pet automatically purges all of its associated tasks from the scheduler.                                                                                
  - Task Scheduling — Create care tasks (feeding, grooming, walks, etc.) linked to a specific pet, with a due date/time and an optional duration in minutes.
  - Recurring Task Auto-Generation — When a recurring task (daily or weekly) is added or when today's tasks are fetched, the scheduler automatically spawns the next
  occurrence for any overdue recurring tasks, using a duplicate-check (matching title + due date) to prevent double-booking.
  - Mark Complete with Auto-Reschedule — Marking a recurring task complete immediately calculates and appends the next due date (current due date + 1 day for daily, + 7 days
   for weekly), again guarded by a duplicate check.
  - Sorted Task View — Retrieve all tasks sorted by due_date, title (alphabetical), or duration (shortest to longest) using Python's built-in sorted() with a lambda key.
  - Time-of-Day Sort — Sort tasks by time of day only (ignoring date) by extracting a zero-padded HH:MM string from each task's due_date and sorting lexicographically.
  - Task Filtering — Filter tasks by completion status (completed=True/False) and/or by pet name. Filters stack sequentially — each narrows the previous result. Passing no
  arguments returns all tasks.
  - Conflict Detection — An O(n²) pairwise scan over all tasks detects two classes of scheduling conflicts:
    - Same-time conflicts — two tasks share an identical due_date.
    - Overlapping-window conflicts — task A starts before task B ends AND task A ends after task B starts, computed as due_date + duration_minutes for each task.
  - Human-Readable Conflict Warnings — warn_conflicts() returns formatted warning strings (e.g., "'Task A' (08:00 AM–08:15 AM) overlaps with 'Task B' (08:10 AM–08:30 AM)")
  rather than raising exceptions, so the UI can display them non-destructively.
  - Owner Schedule View — Owner.get_schedule() filters the central task list to only return tasks whose linked_pet belongs to that owner, keeping the Scheduler
  pet/owner-agnostic.


### Demo

![Game](https://github.com/Sangeetha-007/ai110-module2show-pawpal-starter/blob/main/images/1.png)

![Game2](https://github.com/Sangeetha-007/ai110-module2show-pawpal-starter/blob/main/images/2.png)

![Game3](https://github.com/Sangeetha-007/ai110-module2show-pawpal-starter/blob/main/images/3.png)
