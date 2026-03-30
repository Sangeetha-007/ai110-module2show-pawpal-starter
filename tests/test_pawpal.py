import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler, Conflict


def test_adding_task_increases_pet_task_count():
    scheduler = Scheduler()
    pet = Pet("Simba", "Cat", 7, 15)
    assert len([t for t in scheduler.all_tasks if t.linked_pet == pet]) == 0
    task = Task("Feed Simba", "Hairball food", datetime(2026, 3, 29, 8, 0), linked_pet=pet)
    scheduler.add_task(task)
    assert len([t for t in scheduler.all_tasks if t.linked_pet == pet]) == 1


# The test has two assertions:

# Confirms is_completed starts as False before calling the method
# Confirms it becomes True after mark_complete() is called
def test_mark_complete_changes_status():
    task = Task("Walk Simba", "Evening walk", datetime(2026, 3, 29, 18, 0))
    assert task.is_completed == False
    task.mark_complete()
    assert task.is_completed == True

def test_pet_with_no_tasks_returns_empty():
    scheduler = Scheduler()
    pet = Pet("Luna", "Dog", 3, 20)
    result = [t for t in scheduler.all_tasks if t.linked_pet == pet]
    assert result == []

def test_two_tasks_same_time_detected_as_conflict():
    scheduler = Scheduler()
    pet = Pet("Simba", "Cat", 7, 15)
    same_time = datetime(2026, 4, 1, 9, 0)

    task1 = Task("Feed Simba", "Morning meal", same_time, linked_pet=pet, duration_minutes=15)
    task2 = Task("Groom Simba", "Brush fur", same_time, linked_pet=pet, duration_minutes=15)
    scheduler.add_task(task1)
    scheduler.add_task(task2)

    warnings = scheduler.warn_conflicts()
    assert len(warnings) > 0
    assert "Feed Simba" in warnings[0]
    assert "Groom Simba" in warnings[0]

# Confirm that marking a daily task complete creates a new task for the following day.
def test_completing_daily_task_creates_next_day_task():
    scheduler = Scheduler()
    pet = Pet("Simba", "Cat", 7, 15)
    due = datetime(2026, 4, 1, 8, 0)

    task = Task("Feed Simba", "Breakfast", due, linked_pet=pet, is_recurring=True, recurrence_pattern="daily")
    scheduler.add_task(task)
    scheduler.mark_task_complete(task)

    next_day = due + timedelta(days=1)
    follow_up = [t for t in scheduler.all_tasks if t.title == "Feed Simba" and t.due_date == next_day]
    assert len(follow_up) == 1
    assert follow_up[0].is_completed == False

# Verify that the Scheduler flags duplicate times.
def test_scheduler_flags_duplicate_times():
    scheduler = Scheduler()
    pet = Pet("Simba", "Cat", 7, 15)
    same_time = datetime(2026, 4, 1, 9, 0)

    task1 = Task("Feed Simba", "Morning meal", same_time, linked_pet=pet, duration_minutes=15)
    task2 = Task("Groom Simba", "Brush fur", same_time, linked_pet=pet, duration_minutes=15)
    scheduler.add_task(task1)
    scheduler.add_task(task2)

    conflicts = scheduler.check_for_conflicts()
    assert len(conflicts) == 1
    assert isinstance(conflicts[0], Conflict)
    assert task1 in (conflicts[0].task_a, conflicts[0].task_b)
    assert task2 in (conflicts[0].task_a, conflicts[0].task_b)


def test_get_sorted_tasks_returns_chronological_order():
    scheduler = Scheduler()
    pet = Pet("Simba", "Cat", 7, 15)

    task_afternoon = Task("Groom Simba", "Brush fur", datetime(2026, 4, 1, 14, 0), linked_pet=pet)
    task_morning   = Task("Feed Simba",  "Breakfast", datetime(2026, 4, 1,  8, 0), linked_pet=pet)
    task_evening   = Task("Walk Simba",  "Evening walk", datetime(2026, 4, 1, 18, 0), linked_pet=pet)

    scheduler.add_task(task_afternoon)
    scheduler.add_task(task_morning)
    scheduler.add_task(task_evening)

    sorted_tasks = scheduler.get_sorted_tasks("due_date")

    assert sorted_tasks[0].due_date < sorted_tasks[1].due_date
    assert sorted_tasks[1].due_date < sorted_tasks[2].due_date


