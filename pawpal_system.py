# "logic layer" where all your backend classes live.

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class HealthProfile:
    notes: str = ""


@dataclass
class Pet:
    name: str
    species: str
    age: int
    weight: float
    health_profile: HealthProfile = field(default_factory=HealthProfile)

    # feed, groom, walk prints a confirmation using the pet's name.
    def feed(self):
        """Print a confirmation that this pet has been fed."""
        print(f"{self.name} has been fed.")

    def groom(self):
        """Print a confirmation that this pet has been groomed."""
        print(f"{self.name} has been groomed.")

    def walk(self):
        """Print a confirmation that this pet has been walked."""
        print(f"{self.name} has been walked.")

    def get_health_status(self) -> str:
        """Return a readable summary of the pet's health info."""
        return f"{self.name} | Species: {self.species} | Age: {self.age} | Weight: {self.weight}kg | Notes: {self.health_profile.notes}"


@dataclass
class Task:
    title: str
    description: str
    due_date: datetime
    linked_pet: Optional[Pet] = None
    is_completed: bool = False
    is_recurring: bool = False
    recurrence_pattern: str = ""
    duration_minutes: int = 0

    def mark_complete(self):
        """Mark this task as completed."""
        self.is_completed = True

    def reschedule(self, new_date: datetime):
        """Set a new due date and reset the task to incomplete."""
        self.due_date = new_date
        self.is_completed = False


class Owner:
    def __init__(self, name: str, email: str, scheduler: "Scheduler"):
        self.name = name
        self.email = email
        self.scheduler = scheduler
        self.pets: List[Pet] = []
    #only adds in pet if its already not in the list
    def addPet(self, pet: Pet):
        """Add a pet to this owner's list if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def removePet(self, pet: Pet):
        """Remove a pet and delete all its associated tasks from the scheduler."""
        if pet in self.pets:
            self.pets.remove(pet)
            self.scheduler.all_tasks = [
                task for task in self.scheduler.all_tasks
                if task.linked_pet != pet
            ]

    def get_schedule(self) -> List[Task]:
        """Return all tasks in the scheduler that belong to this owner's pets."""
        return [task for task in self.scheduler.all_tasks
                if task.linked_pet in self.pets]


@dataclass
class Conflict:
    task_a: Task
    task_b: Task


class Scheduler:
    def __init__(self):
        self.all_tasks: List[Task] = []

    def add_task(self, task: Task):
        """Add a task to the scheduler and trigger recurring generation if needed."""
        self.all_tasks.append(task)
        if task.is_recurring:
            self.generate_recurring_tasks()

    def mark_task_complete(self, task: Task):
        """Mark a task complete and auto-schedule the next occurrence for recurring tasks.

        Calls task.mark_complete() to set is_completed = True, then checks
        recurrence_pattern. For 'daily' tasks, the next due date is due_date + 1 day;
        for 'weekly' tasks, due_date + 7 days. A duplicate check (matching title and
        due_date) prevents the same occurrence from being added twice. Non-recurring
        tasks are marked complete with no further action.

        Args:
            task: The Task to mark as complete.
        """
        task.mark_complete()
        if not task.is_recurring:
            return
        if task.recurrence_pattern == "daily":
            next_due = task.due_date + timedelta(days=1)
        elif task.recurrence_pattern == "weekly":
            next_due = task.due_date + timedelta(weeks=1)
        else:
            return
        already_exists = any(
            t.title == task.title and t.due_date == next_due
            for t in self.all_tasks
        )
        if not already_exists:
            self.all_tasks.append(Task(
                title=task.title,
                description=task.description,
                due_date=next_due,
                linked_pet=task.linked_pet,
                is_recurring=task.is_recurring,
                recurrence_pattern=task.recurrence_pattern,
                duration_minutes=task.duration_minutes,
            ))

    # removes a task only if it exists in the list
    def remove_task(self, task: Task):
        """Remove a task from the scheduler if it exists."""
        if task in self.all_tasks:
            self.all_tasks.remove(task)

    # triggers recurring generation first, then returns only incomplete tasks due today
    def get_todays_tasks(self) -> List[Task]:
        """Return all incomplete tasks due today, generating recurring tasks first."""
        self.generate_recurring_tasks()
        today = datetime.now().date()
        return [task for task in self.all_tasks
                if task.due_date.date() == today and not task.is_completed]

    # sorts by "due_date", "title", or "duration"; returns unsorted list as fallback
    def get_sorted_tasks(self, sort_by: str) -> List[Task]:
        """Return all tasks sorted by 'due_date', 'title', or 'duration'."""
        if sort_by == "due_date":
            return sorted(self.all_tasks, key=lambda t: t.due_date)
        elif sort_by == "title":
            return sorted(self.all_tasks, key=lambda t: t.title)
        elif sort_by == "duration":
            return sorted(self.all_tasks, key=lambda t: t.duration_minutes)
        return self.all_tasks

    # compares every pair of tasks; flags a conflict if their time windows overlap using due_date + duration_minutes
    def check_for_conflicts(self) -> List[Conflict]:
        """Return pairs of tasks whose time windows overlap."""
        conflicts = []
        for i, task_a in enumerate(self.all_tasks):
            for task_b in self.all_tasks[i + 1:]:
                a_end = task_a.due_date + timedelta(minutes=task_a.duration_minutes)
                b_end = task_b.due_date + timedelta(minutes=task_b.duration_minutes)
                if task_a.due_date < b_end and a_end > task_b.due_date:
                    conflicts.append(Conflict(task_a, task_b))
        return conflicts

    def warn_conflicts(self) -> List[str]:
        """Return warning messages for tasks scheduled at the same time or with overlapping windows.

        Iterates over every unique pair of tasks (O(n²)) and checks two conditions:
          - Same time: both tasks share an identical due_date.
          - Overlapping window: task A starts before task B ends AND task A ends
            after task B starts, calculated using due_date + duration_minutes.
        Same-time is checked first; overlapping is only reported if the times differ
        but the windows still intersect. Returns human-readable strings rather than
        raising exceptions, so callers can log or display warnings without crashing.

        Returns:
            A list of warning strings; empty if no conflicts are found.
        """
        warnings = []
        for i, task_a in enumerate(self.all_tasks):
            for task_b in self.all_tasks[i + 1:]:
                same_time = task_a.due_date == task_b.due_date
                a_end = task_a.due_date + timedelta(minutes=task_a.duration_minutes)
                b_end = task_b.due_date + timedelta(minutes=task_b.duration_minutes)
                overlapping = task_a.due_date < b_end and a_end > task_b.due_date
                if same_time:
                    warnings.append(
                        f"WARNING: '{task_a.title}' and '{task_b.title}' are both scheduled at "
                        f"{task_a.due_date.strftime('%I:%M %p')} on {task_a.due_date.strftime('%Y-%m-%d')}."
                    )
                elif overlapping:
                    warnings.append(
                        f"WARNING: '{task_a.title}' ({task_a.due_date.strftime('%I:%M %p')}–{a_end.strftime('%I:%M %p')}) "
                        f"overlaps with '{task_b.title}' ({task_b.due_date.strftime('%I:%M %p')}–{b_end.strftime('%I:%M %p')})."
                    )
        return warnings



    #     How it works:
    #   - Starts with the full all_tasks list
    #   - If completed is provided (True/False), filters by task.is_completed
    #   - If pet_name is provided, filters by task.linked_pet.name (guards against None linked pets)
    #   - Both filters stack — each narrows the previous result
    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Filters are applied sequentially and stack — each narrows the previous result.
        Omitting a parameter skips that filter entirely, so calling filter_tasks() with
        no arguments returns all tasks. Tasks with no linked_pet (linked_pet is None)
        are excluded when pet_name is provided.

        Args:
            completed: If True, return only completed tasks. If False, return only
                incomplete tasks. If None (default), completion status is not filtered.
            pet_name: If provided, return only tasks whose linked_pet.name matches
                this string (case-sensitive). If None (default), all pets are included.

        Returns:
            A filtered list of Task objects; empty list if no tasks match.
        """
        results = self.all_tasks
        if completed is not None:
            results = [t for t in results if t.is_completed == completed]
        if pet_name is not None:
            results = [t for t in results if t.linked_pet is not None and t.linked_pet.name == pet_name]
        return results

    def sort_by_time(self) -> List[Task]:
        """Return all tasks sorted by their time of day in HH:MM format.

        Extracts the time portion of each task's due_date as a zero-padded "HH:MM"
        string using strftime, then sorts lexicographically. This works correctly
        because zero-padded 24-hour strings have the same order as numeric time
        (e.g. "08:00" < "09:30" < "14:00" < "23:59"). Note: only time-of-day is
        considered — date is ignored, so tasks on different days may interleave.
        The original all_tasks list is not modified.

        Returns:
            A new list of all Task objects ordered from earliest to latest time of day.
        """
        return sorted(self.all_tasks, key=lambda t: t.due_date.strftime("%H:%M"))

    def generate_recurring_tasks(self):
        """Spawn the next occurrence of any overdue recurring tasks."""
        today = datetime.now().date()
        new_tasks = []
        for task in self.all_tasks:
            if not task.is_recurring or task.recurrence_pattern == "":
                continue
            if task.due_date.date() < today:
                if task.recurrence_pattern == "daily":
                    next_date = task.due_date + timedelta(days=1)
                elif task.recurrence_pattern == "weekly":
                    next_date = task.due_date + timedelta(weeks=1)
                else:
                    continue
                already_exists = any(
                    t.title == task.title and t.due_date == next_date
                    for t in self.all_tasks
                )
                if not already_exists:
                    new_tasks.append(Task(
                        title=task.title,
                        description=task.description,
                        due_date=next_date,
                        linked_pet=task.linked_pet,
                        is_recurring=task.is_recurring,
                        recurrence_pattern=task.recurrence_pattern,
                        duration_minutes=task.duration_minutes
                    ))
        self.all_tasks.extend(new_tasks)


# The Scheduler doesn't need to reach into the Owner's pets — the data flows the other way:


# Scheduler.all_tasks  ←──  all tasks (flat list, central store)
# Task.linked_pet      ←──  each task knows which pet it belongs to
# Owner.get_schedule() ←──  filters scheduler.all_tasks by owner's pets
# The Scheduler is a central store — it holds every task regardless of pet or owner. 
# Retrieval by pet/owner is done by filtering on linked_pet, which already exists in pawpal_system.py:74-76:


# def get_schedule(self) -> List[Task]:
#     return [task for task in self.scheduler.all_tasks
#             if task.linked_pet in self.pets]
# So the pattern is:

# Add tasks into the Scheduler via add_task() with linked_pet set
# Retrieve by owner → call owner.get_schedule()
# Retrieve by pet → filter scheduler.all_tasks where task.linked_pet == some_pet
# The Scheduler intentionally doesn't know about Owners or Pets directly — it just manages tasks. The linked_
# pet field on Task is the bridge that makes filtering possible.