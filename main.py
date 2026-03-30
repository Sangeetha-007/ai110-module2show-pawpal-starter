# temporary "testing ground" to verify your logic works in the terminal.
from pawpal_system import Pet, Owner, Task, Scheduler, HealthProfile
from datetime import datetime

scheduler1 = Scheduler()
owner1 = Owner("Sangeetha", "sangeetha@email.com", scheduler1)
pet1 = Pet("Simba", "Cat", 7, 15)
pet2 = Pet("Mickey", "Cat", 6, 11)
owner1.addPet(pet1)
owner1.addPet(pet2)

# Add tasks OUT OF ORDER (noon, then morning, then evening)
task1 = Task("Grooming Mickey", "Brushing her",          datetime(2026, 3, 29, 12, 0), linked_pet=pet2)
task2 = Task("Feeding Simba",   "Hairball Control Food", datetime(2026, 3, 29,  8, 0), linked_pet=pet1)
task3 = Task("Feeding Mickey",  "Canned Food",           datetime(2026, 3, 29, 10, 0), linked_pet=pet2)
task4 = Task("Walk Simba",      "Evening stroll",        datetime(2026, 3, 29, 18, 0), linked_pet=pet1, is_completed=True)

for task in [task1, task2, task3, task4]:
    scheduler1.add_task(task)

# --- sort_by_time ---
print("=== Sorted by Time ===")
for task in scheduler1.sort_by_time():
    print(f"  [{task.due_date.strftime('%I:%M %p')}] {task.title} ({task.linked_pet.name})")

# --- filter: incomplete only ---
print("\n=== Incomplete Tasks ===")
for task in scheduler1.filter_tasks(completed=False):
    print(f"  {task.title} — completed: {task.is_completed}")

# --- filter: completed only ---
print("\n=== Completed Tasks ===")
for task in scheduler1.filter_tasks(completed=True):
    print(f"  {task.title} — completed: {task.is_completed}")

# --- filter: by pet name ---
print("\n=== Tasks for Simba ===")
for task in scheduler1.filter_tasks(pet_name="Simba"):
    print(f"  {task.title}")

# --- filter: both together (incomplete tasks for Mickey) ---
print("\n=== Incomplete Tasks for Mickey ===")
for task in scheduler1.filter_tasks(completed=False, pet_name="Mickey"):
    print(f"  {task.title}")

# --- conflict detection ---
print("\n=== Conflict Detection ===")
conflict_scheduler = Scheduler()

# Same-time conflict (exact same due_date, no duration)
t_same_a = Task("Feed Simba",   "Morning kibble", datetime(2026, 3, 29, 8, 0), linked_pet=pet1)
t_same_b = Task("Groom Simba",  "Brush coat",     datetime(2026, 3, 29, 8, 0), linked_pet=pet1)
# Overlapping window conflict (walk starts before feeding ends)
t_over_a = Task("Walk Mickey",  "Park loop",      datetime(2026, 3, 29, 10, 0), linked_pet=pet2, duration_minutes=60)
t_over_b = Task("Feed Mickey",  "Canned food",    datetime(2026, 3, 29, 10, 30), linked_pet=pet2, duration_minutes=15)

for t in [t_same_a, t_same_b, t_over_a, t_over_b]:
    conflict_scheduler.add_task(t)

warnings = conflict_scheduler.warn_conflicts()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

# --- mark_task_complete: recurring daily task auto-spawns next occurrence ---
print("\n=== Recurring Task Auto-Spawn ===")
daily_task = Task("Feed Simba", "Morning kibble", datetime(2026, 3, 29, 8, 0),
                  linked_pet=pet1, is_recurring=True, recurrence_pattern="daily")
scheduler1.add_task(daily_task)
print(f"Before: {len(scheduler1.filter_tasks(pet_name='Simba'))} Simba tasks")
scheduler1.mark_task_complete(daily_task)
simba_tasks = scheduler1.filter_tasks(pet_name="Simba")
print(f"After:  {len(simba_tasks)} Simba tasks")
for t in sorted(simba_tasks, key=lambda t: t.due_date):
    status = "done" if t.is_completed else "pending"
    print(f"  [{t.due_date.strftime('%Y-%m-%d %I:%M %p')}] {t.title} — {status}")
