import streamlit as st
from pawpal_system import Task, Pet, Scheduler, Owner
from datetime import datetime


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.scheduler = Scheduler()
    st.session_state.owner = Owner("Sangeetha", "sangeetha@email.com", st.session_state.scheduler)

    pet1 = Pet("Simba", "Cat", 7, 15)
    pet2 = Pet("Mickey", "Cat", 6, 11)
    st.session_state.owner.addPet(pet1)
    st.session_state.owner.addPet(pet2)

    task1 = Task("Feeding Simba", "Hairball Control Dry Food", datetime(2026, 3, 29, 8, 0), linked_pet=pet1)
    task2 = Task("Feeding Mickey", "Canned Food", datetime(2026, 3, 29, 10, 0), linked_pet=pet2)
    task3 = Task("Grooming Mickey", "Brushing her", datetime(2026, 3, 29, 12, 0), linked_pet=pet2)
    st.session_state.scheduler.add_task(task1)
    st.session_state.scheduler.add_task(task2)
    st.session_state.scheduler.add_task(task3)

st.markdown("### Pets")
for pet in st.session_state.owner.pets:
    st.write(f"- {pet.name} ({pet.species}, Age: {pet.age})")

st.divider()

st.subheader("Today's Schedule")
tasks = st.session_state.owner.get_schedule()
if tasks:
    for task in tasks:
        st.write(f"[{task.due_date.strftime('%I:%M %p')}] {task.title} — {task.description}")
else:
    st.info("No tasks scheduled.")
