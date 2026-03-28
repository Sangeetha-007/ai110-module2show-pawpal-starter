# "logic layer" where all your backend classes live.

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
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

    def feed(self):
        pass

    def groom(self):
        pass

    def walk(self):
        pass

    def get_health_status(self) -> str:
        pass


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
        pass

    def reschedule(self, new_date: datetime):
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: List[Pet] = []

    def addPet(self, pet: Pet):
        pass

    def removePet(self, pet: Pet):
        pass

    def get_schedule(self) -> List[Task]:
        pass


@dataclass
class Conflict:
    task_a: Task
    task_b: Task


class Scheduler:
    def __init__(self):
        self.all_tasks: List[Task] = []

    def add_task(self, task: Task):
        pass

    def remove_task(self, task: Task):
        pass

    def get_todays_tasks(self) -> List[Task]:
        pass

    def get_sorted_tasks(self, sort_by: str) -> List[Task]:
        pass

    def check_for_conflicts(self) -> List[Conflict]:
        pass

    def generate_recurring_tasks(self):
        pass
