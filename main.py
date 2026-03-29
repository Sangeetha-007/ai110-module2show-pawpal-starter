# temporary "testing ground" to verify your logic works in the terminal.
from pawpal_system import Pet, Owner, Task, Scheduler, HealthProfile
from datetime import datetime

scheduler1=Scheduler()
owner1=Owner("Sangeetha", "sangeetha@email.com", scheduler1)
pet1=Pet("Simba", "Cat", 7, 15)
pet2=Pet("Mickey", "Cat", 6, 11)

#Add 3 tasks
task1=Task("Feeding Simba", "Hairball Control Dry Food", datetime(2026, 3, 29, 8, 0))
task2=Task("Feeding Mickey", "Canned Food", datetime(2026, 3, 29, 10, 0))
task3=Task("Grooming Mickey", "Brushing her", datetime(2026, 3, 29, 12, 0))

print("Today's Schedule:")
for task in [task1, task2, task3]:
    print(f"  [{task.due_date.strftime('%I:%M %p')}] {task.title} — {task.description}")

