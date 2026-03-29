import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from pawpal_system import Task, Pet, Scheduler


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
