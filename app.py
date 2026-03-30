import streamlit as st
from pawpal_system import Task, Pet, Scheduler, Owner
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Seed session state once ---
if "owner" not in st.session_state:
    st.session_state.scheduler = Scheduler()
    st.session_state.owner = Owner("Sangeetha", "sangeetha@email.com", st.session_state.scheduler)

    pet1 = Pet("Simba", "Cat", 7, 15)
    pet2 = Pet("Mickey", "Cat", 6, 11)
    st.session_state.owner.addPet(pet1)
    st.session_state.owner.addPet(pet2)

    today = datetime.now().replace(second=0, microsecond=0)
    task1 = Task("Feeding Simba",  "Hairball Control Dry Food", today.replace(hour=8,  minute=0),  linked_pet=pet1, duration_minutes=15, is_recurring=True, recurrence_pattern="daily")
    task2 = Task("Feeding Mickey", "Canned Food",               today.replace(hour=8,  minute=10), linked_pet=pet2, duration_minutes=20)
    task3 = Task("Grooming Mickey","Brushing her",              today.replace(hour=12, minute=0),  linked_pet=pet2, duration_minutes=30)
    task4 = Task("Walk Simba",     "Evening walk",              today.replace(hour=18, minute=0),  linked_pet=pet1, duration_minutes=45)
    for t in (task1, task2, task3, task4):
        st.session_state.scheduler.add_task(t)

scheduler: Scheduler = st.session_state.scheduler
owner: Owner = st.session_state.owner

# --- Pets ---
st.subheader("Pets")
for pet in owner.pets:
    st.write(f"- **{pet.name}** ({pet.species}, Age: {pet.age})")

st.divider()

# --- Controls ---
st.subheader("Schedule")
col1, col2 = st.columns(2)
with col1:
    sort_by = st.selectbox("Sort by", ["due_date", "title", "duration"], index=0)
with col2:
    pet_names = ["All pets"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Filter by pet", pet_names)

# --- Build display data ---
sorted_tasks = scheduler.get_sorted_tasks(sort_by)

if pet_filter != "All pets":
    sorted_tasks = [t for t in sorted_tasks if t.linked_pet and t.linked_pet.name == pet_filter]

if sorted_tasks:
    rows = [
        {
            "Time": t.due_date.strftime("%I:%M %p"),
            "Task": t.title,
            "Pet": t.linked_pet.name if t.linked_pet else "—",
            "Duration": f"{t.duration_minutes} min" if t.duration_minutes else "—",
            "Recurring": "Yes" if t.is_recurring else "No",
            "Done": "✓" if t.is_completed else "",
        }
        for t in sorted_tasks
    ]
    st.table(rows)
else:
    st.info("No tasks match the current filter.")

st.divider()

# --- Conflict warnings ---
st.subheader("Conflict Check")
warnings = scheduler.warn_conflicts()
if warnings:
    for w in warnings:
        # strip the leading "WARNING: " prefix for cleaner Streamlit display
        st.warning(w.removeprefix("WARNING: "))
else:
    st.success("No scheduling conflicts detected.")
