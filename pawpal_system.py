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
        print(f"{self.name} has been fed.")

    def groom(self):
        print(f"{self.name} has been groomed.")

    def walk(self):
        print(f"{self.name} has been walked.")

    def get_health_status(self) -> str:
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
        self.is_completed = True

    def reschedule(self, new_date: datetime):
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
        if pet not in self.pets:
            self.pets.append(pet)

    def removePet(self, pet: Pet):
        if pet in self.pets:
            self.pets.remove(pet)
            self.scheduler.all_tasks = [
                task for task in self.scheduler.all_tasks
                if task.linked_pet != pet
            ]

    def get_schedule(self) -> List[Task]:
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
        self.all_tasks.append(task)
        if task.is_recurring:
            self.generate_recurring_tasks()
    # removes a task only if it exists in the list
    def remove_task(self, task: Task):
        if task in self.all_tasks:
            self.all_tasks.remove(task)

    # triggers recurring generation first, then returns only incomplete tasks due today
    def get_todays_tasks(self) -> List[Task]:
        self.generate_recurring_tasks()
        today = datetime.now().date()
        return [task for task in self.all_tasks
                if task.due_date.date() == today and not task.is_completed]

    # sorts by "due_date", "title", or "duration"; returns unsorted list as fallback
    def get_sorted_tasks(self, sort_by: str) -> List[Task]:
        if sort_by == "due_date":
            return sorted(self.all_tasks, key=lambda t: t.due_date)
        elif sort_by == "title":
            return sorted(self.all_tasks, key=lambda t: t.title)
        elif sort_by == "duration":
            return sorted(self.all_tasks, key=lambda t: t.duration_minutes)
        return self.all_tasks

    # compares every pair of tasks; flags a conflict if their time windows overlap using due_date + duration_minutes
    def check_for_conflicts(self) -> List[Conflict]:
        conflicts = []
        for i, task_a in enumerate(self.all_tasks):
            for task_b in self.all_tasks[i + 1:]:
                a_end = task_a.due_date + timedelta(minutes=task_a.duration_minutes)
                b_end = task_b.due_date + timedelta(minutes=task_b.duration_minutes)
                if task_a.due_date < b_end and a_end > task_b.due_date:
                    conflicts.append(Conflict(task_a, task_b))
        return conflicts

    def generate_recurring_tasks(self):
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