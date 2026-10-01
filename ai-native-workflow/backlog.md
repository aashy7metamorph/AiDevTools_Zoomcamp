# Implementation Backlog

## T1 — Django project & app scaffold
Objective: Set up a minimal, runnable Django project and one app for household chores, wired so tests can run.
Acceptance criteria refs: none directly; enables all others
Dependencies: none

## T2 — Household member support (F1)
Objective: A household member can be added by name; saved members are listed and available for selection.
Acceptance criteria refs: AC1
Dependencies: T1

## T3 — Create and assign chores (F2)
Objective: A chore can be created with a title and assigned to exactly one existing household member in one action; new chores start as pending.
Acceptance criteria refs: AC2, AC3
Dependencies: T2

## T4 — Shared board (F4, part 1)
Objective: One shared board lists all chores with title, assigned member, and status; pending and completed are visually distinguishable.
Acceptance criteria refs: AC4
Dependencies: T3

## T5 — Completion action (F3)
Objective: A pending chore can be marked completed with one Done action; no enforcement of who performs it.
Acceptance criteria refs: AC5, AC7
Dependencies: T4

## T6 — Member filtering (F4, part 2)
Objective: The board can optionally be filtered to show only chores assigned to a selected member.
Acceptance criteria refs: AC6
Dependencies: T4

## T7 — Full verification pass
Objective: Run the full test suite against the implemented product; confirm all acceptance criteria hold end-to-end.
Acceptance criteria refs: AC1–AC7
Dependencies: T1–T6