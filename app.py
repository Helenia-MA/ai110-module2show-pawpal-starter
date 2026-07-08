from datetime import date, time

import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler, PRIORITY_VALUES, PRIORITY_LABELS
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ — a pet-care planning assistant.

Add your pets and their care tasks, then generate a daily plan that respects each pet's
time budget and priorities, explains its reasoning, and warns about scheduling conflicts.
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

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

# Create the Owner once and keep it in the session vault; reuse it every rerun.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner

# One scheduler and one notion of "today" for the whole render.
scheduler = Scheduler()
today = date.today()

# Show and clear any one-off message stashed before a st.rerun() (see "Done").
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

st.divider()

# --- Add a pet -----------------------------------------------------------
st.subheader("Add a pet")
col1, col2, col3 = st.columns(3)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    new_species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    pet_minutes = st.number_input("Time available (min)", min_value=0, max_value=600, value=60)

if st.button("Add pet"):
    owner.add_pet(new_pet_name, new_species, int(pet_minutes))
    st.success(f"Added {new_pet_name} to {owner.name}.")

st.divider()

# --- Add a task to a pet -------------------------------------------------
st.subheader("Add a task")
if not owner.pets:
    st.info("Add a pet first, then you can give it tasks.")
else:
    pet_names = [pet.name for pet in owner.pets]
    chosen_pet = st.selectbox("Which pet?", pet_names)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col4, col5 = st.columns(2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly"])
    with col5:
        task_time = st.time_input("Time", value=time(9, 0))

    if st.button("Add task"):
        # Find the chosen pet, then add the task using our real method.
        pet = owner.pets[pet_names.index(chosen_pet)]
        pet.add_task(
            task_title,
            int(duration),
            PRIORITY_VALUES[priority],
            frequency=frequency,
            time=task_time.strftime("%H:%M"),
        )
        st.success(f"Added '{task_title}' to {pet.name}.")

st.divider()

# --- Current pets & tasks ------------------------------------------------
st.subheader("Current pets & tasks")
if not owner.pets:
    st.info("No pets yet. Add one above.")
else:
    for pet in owner.pets:
        st.markdown(
            f"**{pet.name}** ({pet.species}) — {pet.available_minutes} min available"
        )
        if pet.tasks:
            # Iterate a snapshot: completing a task appends a new one to pet.tasks,
            # and we don't want to mutate the list we're looping over.
            for t in list(pet.tasks):
                c1, c2, c3, c4, c5 = st.columns([2, 4, 2, 2, 2])
                c1.write(t.time)
                c2.write(f"{t.name} ({t.frequency})")
                c3.write(f"{t.duration_minutes} min")
                c4.write(PRIORITY_LABELS[t.priority])
                if t.completed:
                    c5.write("✓ done")
                elif c5.button("Done", key=f"done_{pet.name}_{t.id}"):
                    # Mark complete; for a recurring task this spawns the next one.
                    new = scheduler.complete_task(pet, t.id, today)
                    if new is not None:
                        st.session_state["flash"] = (
                            f"Completed '{t.name}'. Next {new.frequency} occurrence "
                            f"scheduled for {new.due_date}."
                        )
                    else:
                        st.session_state["flash"] = f"Completed '{t.name}'."
                    st.rerun()
        else:
            st.caption("No tasks yet.")

st.divider()

st.subheader("Build schedule")
st.caption("Plans each pet against its time budget, honoring priority, and flags conflicts.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.info("Add a pet and some tasks first.")
    else:
        # Owner-wide time conflicts: two tasks (same or different pets) at once.
        time_conflicts = scheduler.detect_time_conflicts(owner, today)
        for warning in time_conflicts:
            st.warning(f"⏰ {warning}")

        plans = scheduler.all_owner_plans(owner, today)
        for pet, plan in plans.items():
            st.markdown(f"### {pet.name} ({pet.species}) — {pet.available_minutes} min")

            # Per-pet conflicts (over budget, duplicate task names).
            for warning in scheduler.detect_conflicts(pet, today):
                st.warning(warning)

            if plan:
                for t in plan:
                    st.write(
                        f"- **{t.time}**  {t.name} — {t.duration_minutes} min "
                        f"[{PRIORITY_LABELS[t.priority]}]"
                    )
            else:
                st.caption("Nothing scheduled today.")

            # Reasoning: summarize planned vs. the due tasks that didn't fit.
            skipped = [t for t in pet.tasks if t.needs_doing(today) and t not in plan]
            st.text(scheduler.explain(plan, skipped, pet.available_minutes))
