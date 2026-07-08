"""Tests for PawPal+ core behaviors."""

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    """Task Completion: mark_complete() flips the task from not-done to done."""
    task = Task(id=1, name="Walk", duration_minutes=30, priority=3)

    # A new task starts incomplete...
    assert task.completed is False

    task.mark_complete()

    # ...and mark_complete() sets it to done.
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    """Task Addition: adding a task to a Pet grows that pet's task list by one."""
    pet = Pet("Biscuit", "dog", available_minutes=60)

    # No tasks to start.
    assert len(pet.tasks) == 0

    pet.add_task("Morning walk", 30, 3)

    # One task after adding.
    assert len(pet.tasks) == 1
