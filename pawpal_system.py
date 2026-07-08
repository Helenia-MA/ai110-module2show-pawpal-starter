"""PawPal+ — class skeleton generated from diagrams/uml.mmd.

Skeleton only: names, attributes, and empty method stubs. No logic yet
(README step 3). Fill in the method bodies during the implementation step.
"""

from dataclasses import dataclass, field


# Priority is stored as a NUMBER internally (higher = more important) so tasks
# sort naturally. The UI translates to/from labels using these mappings.
PRIORITY_LABELS = {3: "high", 2: "medium", 1: "low"}
PRIORITY_VALUES = {label: value for value, label in PRIORITY_LABELS.items()}


@dataclass
class Task:
    """A single pet-care task. Data only — no behavior."""

    id: int
    name: str
    duration_minutes: int
    priority: int


class Pet:
    """A pet, its care tasks, and how much time the owner has for it today.

    Each pet manages its own tasks and carries its own available_minutes, so the
    owner can allocate time per pet (e.g. 60 min for the dog, 30 for the cat).
    """

    def __init__(self, name: str, species: str = "", available_minutes: int = 0) -> None:
        self.name: str = name
        self.species: str = species
        self.available_minutes: int = available_minutes
        self.tasks: list[Task] = []
        # Counter so each task gets a unique, deterministic id (1, 2, 3...).
        self._next_id: int = 1

    def add_task(self, name: str, duration_minutes: int, priority: int) -> Task:
        """Create a Task with the next id, append it, and return it."""
        pass

    def edit_task(
        self,
        id: int,
        name: str | None = None,
        duration_minutes: int | None = None,
        priority: int | None = None,
    ) -> Task:
        """Find the task with this id and update the fields that were provided."""
        pass

    def set_availability(self, minutes: int) -> None:
        """Set how many minutes the owner has for this pet today."""
        pass


class Owner:
    """Holds the owner's pets. Time is allocated per pet (see Pet.available_minutes)."""

    def __init__(self, name: str = "") -> None:
        self.name: str = name
        self.pets: list[Pet] = []

    def add_pet(self, name: str, species: str = "", available_minutes: int = 0) -> Pet:
        """Create a Pet (with its own time budget), append it, and return it."""
        pass


class Scheduler:
    """Turns a list of tasks + a time budget into an ordered daily plan.

    Strategy (from the design):
      - Sort strictly by priority (high first), then shortest-duration as tie-break.
      - "Skip and keep going": if a task doesn't fit the remaining time, skip it
        and try the next, so leftover minutes aren't wasted. Greedy, not optimal.
    """

    def build_plan(self, tasks: list[Task], available_minutes: int) -> list[Task]:
        """Front door for ONE task list: sort, then filter to what fits."""
        pass

    def build_plans_for_owner(self, owner: "Owner") -> dict[Pet, list[Task]]:
        """Plan every pet separately: one schedule per pet, keyed by pet."""
        pass

    def _sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Sort by priority (high first), then by shortest duration."""
        pass

    def _filter_to_fit(
        self, sorted_tasks: list[Task], available_minutes: int
    ) -> list[Task]:
        """Walk the sorted tasks, keeping each that still fits; skip the rest."""
        pass

    def explain(
        self,
        planned: list[Task],
        skipped: list[Task],
        available_minutes: int,
    ) -> str:
        """Human-readable reasoning: what was planned, what was skipped and why."""
        pass
