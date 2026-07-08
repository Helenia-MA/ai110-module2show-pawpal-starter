"""PawPal+ testing ground.

Run with:  python main.py

Builds a small owner/pets/tasks scenario and prints today's schedule for each
pet to the terminal, along with the scheduler's reasoning.
"""

from pawpal_system import Owner, Scheduler, PRIORITY_VALUES, PRIORITY_LABELS

# Shorthand so we can read tasks as high/medium/low instead of 3/2/1.
HIGH = PRIORITY_VALUES["high"]
MEDIUM = PRIORITY_VALUES["medium"]
LOW = PRIORITY_VALUES["low"]


def build_sample_owner() -> Owner:
    """Create one owner with two pets and a handful of tasks each."""
    owner = Owner("Jordan")

    # Two pets, each with its own daily time budget.
    biscuit = owner.add_pet("Biscuit", "dog", available_minutes=60)
    mochi = owner.add_pet("Mochi", "cat", available_minutes=30)

    # Tasks with a range of durations and priorities.
    biscuit.add_task("Morning walk", 30, HIGH)
    biscuit.add_task("Medication", 10, HIGH)
    biscuit.add_task("Brushing", 25, LOW)      # likely won't fit the 60 min budget

    mochi.add_task("Feeding", 10, HIGH)
    mochi.add_task("Litter change", 15, MEDIUM)
    mochi.add_task("Play time", 20, LOW)       # likely won't fit the 30 min budget

    return owner


def print_schedule(owner: Owner) -> None:
    """Print 'Today's Schedule' for every pet, with the scheduler's reasoning."""
    scheduler = Scheduler()
    plans = scheduler.all_owner_plans(owner)

    print("=" * 48)
    print(f"Today's Schedule for {owner.name}")
    print("=" * 48)

    for pet, plan in plans.items():
        print(f"\n{pet.name} ({pet.species}) - {pet.available_minutes} min available")
        print("-" * 48)

        if plan:
            for task in plan:
                print(f"  [ ] {task.name:<16} {task.duration_minutes:>3} min [priority: {PRIORITY_LABELS[task.priority]}]")
        else:
            print("  (nothing scheduled today)")

        # Reasoning: what was planned vs. skipped, and why.
        skipped = [t for t in pet.tasks if t not in plan]
        print()
        print(scheduler.explain(plan, skipped, pet.available_minutes))


if __name__ == "__main__":
    owner = build_sample_owner()
    print_schedule(owner)
