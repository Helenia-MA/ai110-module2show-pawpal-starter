"""PawPal+ — class skeleton generated from diagrams/uml.mmd.
"""

from dataclasses import dataclass


# Priority is stored as a NUMBER internally (higher = more important) so tasks
# sort naturally. The UI translates to/from labels using these mappings.
PRIORITY_LABELS = {3: "high", 2: "medium", 1: "low"}
PRIORITY_VALUES = {label: value for value, label in PRIORITY_LABELS.items()}


@dataclass
class Task:
    """A single pet-care task."""
    id: int
    name: str
    duration_minutes: int
    priority: int
    frequency: str = "daily"   # e.g. "daily", "weekly"
    completed: bool = False
    # NOTE (known limitation): `completed` has no date context, so recurring
    # tasks don't auto-reset across days. Future: replace with a `last_completed`
    # date + a `needs_doing(today)` check that derives due-ness from `frequency`.

    def mark_complete(self) -> None:
        """Mark this task as done for today."""
        self.completed = True


class Pet:
    """A pet, its care tasks, and how much time the owner has for it today.

    Each pet manages its own tasks and carries its own available_minutes, so the
    owner can allocate time per pet (e.g. 60 min for the dog, 30 for the cat).
    """

    def __init__(self, name: str, species: str = "", available_minutes: int = 0) -> None:
        """Create a pet with an empty task list and its own time budget."""
        self.name: str = name
        self.species: str = species
        self.available_minutes: int = available_minutes
        self.tasks: list[Task] = []
        # Counter so each task gets a unique, deterministic id (1, 2, 3...).
        self._next_id: int = 1

    def add_task(
        self,
        name: str,
        duration_minutes: int,
        priority: int,
        frequency: str = "daily",
    ) -> Task:
        """Create a Task with the next id, append it, and return it."""
        task = Task(self._next_id, name, duration_minutes, priority, frequency)
        self._next_id += 1
        self.tasks.append(task)
        return task

    def edit_task(
        self,
        id: int,
        name: str | None = None,
        duration_minutes: int | None = None,
        priority: int | None = None,
        frequency: str | None = None,
        completed: bool | None = None,
    ) -> Task:
        """Find the task with this id and update the fields that were provided."""
        for task in self.tasks:
            if task.id == id:
                if name is not None:
                    task.name = name
                if duration_minutes is not None:
                    task.duration_minutes = duration_minutes
                if priority is not None:
                    task.priority = priority
                if frequency is not None:
                    task.frequency = frequency
                if completed is not None:
                    task.completed = completed
                return task
        raise ValueError(f"No task with id {id}")

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has for this pet today."""
        self.available_minutes = minutes


class Owner:
    """Holds the owner's pets. Time is allocated per pet (see Pet.available_minutes)."""

    def __init__(self, name: str = "") -> None:
        """Create an owner with an empty list of pets."""
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, name: str, species: str = "", available_minutes: int = 0) -> Pet:
        """Create a Pet (with its own time budget), append it, and return it."""
        pet = Pet(name, species, available_minutes)
        self.pets.append(pet)
        return pet

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of the owner's pets, in one flat list."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Turns a list of tasks + a time budget into an ordered daily plan.

    Strategy (from the design):
      - Sort strictly by priority (high first), then shortest-duration as tie-break.
      - "Skip and keep going": if a task doesn't fit the remaining time, skip it
        and try the next, so leftover minutes aren't wasted. Greedy, not optimal.
    """

    def build_plan(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Sort by priority then shortest duration, then keep what fits the budget.

        Uses "skip and keep going": a task that doesn't fit is skipped, and we
        keep checking later (shorter) tasks so leftover minutes aren't wasted.
        Already-completed tasks are excluded — we only plan what's still to do.
        """
        # Drop completed tasks, then sort: highest priority first (-priority),
        # then shortest duration first.
        pending = [t for t in tasks if not t.completed]
        ordered = sorted(pending, key=lambda t: (-t.priority, t.duration_minutes))

        plan: list[Task] = []
        used = 0
        for task in ordered:
            if used + task.duration_minutes <= available_minutes:
                plan.append(task)
                used += task.duration_minutes
        return plan

    def all_owner_plans(self, owner: "Owner") -> dict[Pet, list[Task]]:
        """Plan every pet separately: one schedule per pet, keyed by pet."""
        return {
            pet: self.build_plan(pet.tasks, pet.available_minutes)
            for pet in owner.pets
        }

    def explain(
        self,
        planned: list[Task],
        skipped: list[Task],
        available_minutes: int,
    ) -> str:
        """Human-readable reasoning: what was planned, what was skipped and why.

        `skipped` is any task not in the plan (didn't fit, or already completed);
        each task's own `completed` flag tells us which reason to show.
        """
        used = sum(t.duration_minutes for t in planned)
        total = len(planned) + len(skipped)
        free = available_minutes - used

        lines = [
            f"Planned {len(planned)} of {total} task(s) — "
            f"{used} of {available_minutes} min used ({free} min free)."
        ]

        if planned:
            lines.append("")
            lines.append("Included:")
            for t in planned:
                label = PRIORITY_LABELS.get(t.priority, str(t.priority))
                lines.append(f"  • {t.name} — {t.duration_minutes} min [{label}]")

        if skipped:
            lines.append("")
            lines.append("Skipped:")
            for t in skipped:
                label = PRIORITY_LABELS.get(t.priority, str(t.priority))
                reason = "already completed" if t.completed else "didn't fit remaining time"
                lines.append(
                    f"  • {t.name} — {t.duration_minutes} min [{label}] ({reason})"
                )

        return "\n".join(lines)
