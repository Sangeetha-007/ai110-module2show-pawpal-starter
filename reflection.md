# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform are adding a pet, tracking a feeding schedule and tracking daily grooming. If the pet is long haired, it may need grooming. If the pet is short haired, grooming daily may not be mandatory. 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


My UML diagram includes the classes: Owner, Pet, Task and Scheduler. The Owner class includes name and email as string. It holds a list of pets in case someone has multiple pets (it is of type Pet). It also includes an addPet and removePet in case a pet is added by mistake, etc. Also, has get_schedule which is of type "Task" for the owner. 

The pet class includes a name, the species, age and weight. It includes a health profile to track the pet's wellness. Additionally, it has the feed, groom, walk and get_health_status methods. 

The next class that was created is "Task". Task has a description, due_date, is_completed (to check if it was completed), is_recurring, recurrence_pattern, and duration_minutes. Task has a linked_pet of type Pet. It answers "which pet is this task for". It also has a mark_complete method and a reschedule method. 

The final class is Scheduler. It has a title, description, due_date, is_completed, is_recurring, recurrence_pattern and duration_minutes. It has a linked_pet of type Pet. Also, it has a mark_complete and a reschedule. 

My UML diagram: 

classDiagram
    class Owner {
        +String name
        +String email
        +List<Pet> pets
        +addPet(pet: Pet)
        +removePet(pet: Pet)
        +get_schedule(): List<Task>
    }

    class Pet {
        +String name
        +String species
        +int age
        +float weight
        +HealthProfile health_profile
        +feed()
        +groom()
        +walk()
        +get_health_status(): String
    }

    class Task {
        +String title
        +String description
        +DateTime due_date
        +bool is_completed
        +bool is_recurring
        +String recurrence_pattern
        +int duration_minutes
        +Pet linked_pet
        +mark_complete()
        +reschedule(new_date: DateTime)
    }

    class Scheduler {
        +List<Task> all_tasks
        +add_task(task: Task)
        +remove_task(task: Task)
        +get_todays_tasks(): List<Task>
        +get_sorted_tasks(sort_by: String): List<Task>
        +check_for_conflicts(): List<Conflict>
        +generate_recurring_tasks()
    }

    Owner "1" *-- "many" Pet : owns
    Pet "1" *-- "many" Task : has
    Scheduler "1" o-- "many" Task : manages


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

A missing relationship Claude suggested for me is to give Pet a tasks list. It said:
"Pet has no tasks list — Task.linked_pet links a task to a pet, but you can't go the other direction (pet.tasks). The UML's Pet "1" *-- "many" Task implies both directions should be navigable."
I replied to it by asking: 
"Why should pet have a task when a pet isnt the one doing the task? the owner has to do the task for the pet."
Claude ended up agreeing with me and said:
"That's a fair point. The task is performed by the owner, but it's performed for the pet — so linked_pet on Task is the right relationship (task → pet reference), not a tasks list on Pet.

The UML relationship Pet "1" *-- "many" Task is a bit misleading in that sense — it likely just means "a pet is associated with many tasks", not that the pet owns or initiates them.

So scratch that first missing relationship — it's not actually needed."
Therefore I did not give Pet a tasks list. 

Another missing relationship that Claude told me about is:
"Owner has no reference to Scheduler — Owner.get_schedule() has nothing to query. There's no way for an owner to reach their tasks without a scheduler attached."

I implemented this suggestion in get_scheduler and the Owner class inside of pawpal_system.py. 

The logic bottlenecks suggested to be fixed by Claude are:
generate_recurring_tasks() has no trigger — If it's only called manually, recurring tasks silently won't exist until someone remembers to call it. It should be invoked inside get_todays_tasks() or add_task().

No cascade when removing a pet — Owner.removePet() doesn't clean up that pet's tasks from the Scheduler, leaving orphaned Task objects where linked_pet points to a pet that no longer exists.

I implemented generate_recurring_tasks() with the help of Claude. 


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---
One tradeoff my scheduler makes is sort_by_time sorts by the time of day only. It ignores the date/day. 
This means a task due tomorrow at 8am sorts before one due today at 8pm. This tradeoff is reasonable for the scenario because I am assuming the owner/user is only looking at tasks of the day and not tasks of the next day. I hope to keep my methods as simple as I can, without adding more complexity so I am assuming the tradeoff is reasonable for now. 

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
