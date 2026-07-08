# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

```
================================================
Today's Schedule for Jordan
================================================

Biscuit (dog) - 60 min available
------------------------------------------------
  [ ] Medication        10 min [priority: high]
  [ ] Morning walk      30 min [priority: high]

Planned 2 of 3 task(s) — 40 of 60 min used (20 min free).

Included:
  • Medication — 10 min [high]
  • Morning walk — 30 min [high]

Skipped:
  • Brushing — 25 min [low] (didn't fit remaining time)

Mochi (cat) - 30 min available
------------------------------------------------
  [ ] Feeding           10 min [priority: high]
  [ ] Litter change     15 min [priority: medium]

Planned 2 of 3 task(s) — 25 of 30 min used (5 min free).

Included:
  • Feeding — 10 min [high]
  • Litter change — 15 min [medium]

Skipped:
  • Play time — 20 min [low] (didn't fit remaining time)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# ==================================================================================================== test session starts =====================================================================================================
platform darwin -- Python 3.13.10, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/Admin/Desktop/SUMMER 2026/CODEPATH/AI110/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 18 items

tests/test_pawpal.py ..................                                                                                                                                                                                [100%]

===================================================================================================== 18 passed in 0.03s =====================================================================================================
(.venv) .../ai110-module2show-pawpal-starter>
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

1. task sorting
    Scheduler.sort_by_time() - orders tasks by their time
    Scheduler.sort_by_duration() - orders tasks by their duration(duration_minutes);(ascending order; shortest - longest)
    Scheduler.build_plan() - selects tasks by priority then shortest duration and returns the chosen plan sorted by the tasks' time
2. filtering
    Owner.tasks_for_pet() - filter by pet
    Scheduler.filter_by-status - filter by completion status
    Task.needs_doing() - helps with filtering what's due today
3. conflict detection
    Scheduler.detect_time_conflict() - detects clash in exact time for tasks for a given owner across all pets
    Scheduler.detect_conflicts() - checks for exceeded time availability and duplicate task names for a given pet
4. recurring task logic
    Scheduler.complete_task() - marks a task completed, spawns new occurrence for recurring ones based on their frequency
    Task.mark_complete() - marks the task occurrence done
    Task.due_date() - the day when a spawned occurrence is due
    FREQUENCY_DAYS - for mapping the frequencies to numerical values eg daily, weekly etc
5. planning and explanation
    Scheduler.build_plan() - makes the daily plan per pet within the time budget
    Scheduler.all_owner_plans() - maps each plan to its respective pet
    Scheduler.explain() - provides reasoning for the order of the tasks and a summary of what was planned or skipped and why


## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
