# Shared Household Chores — Product Plan

## 1. Problem Statement

A single household needs a simple shared place to assign chores to named members and track whether those chores are pending or completed. Without such a place, coordination happens out of band and it is easy to lose track of who is responsible for what and whether it is done.

## 2. Scope

This is a deliberately small, single-household chore-management application. It provides one shared board where members can be named, chores can be created and assigned, and completion can be tracked.

## 3. Users

- Household members are represented by names.
- There is exactly one household.
- There are no accounts.
- There is no authentication.
- There is no current-user concept.
- Because there is no authentication, the application does not technically enforce which person performs an action.

## 4. Core Features

### F1 — Manage household members

- Add household members by name.
- Saved members can be selected when assigning chores.
- No editing/removing members, accounts, roles, or permissions.

### F2 — Create and assign chores

- Create a chore with a title.
- Assign the chore to exactly one existing household member during creation.
- No claiming, reassignment, editing, deletion, recurrence, scheduling, or reminders.

### F3 — Track completion

- New chores start as pending.
- A pending chore can be marked completed using one Done action.
- The assigned member is conceptually responsible for the chore.
- Because there is no authentication, the application does not enforce who clicks Done.
- No approval, confirmation, reopening, or completion authorization.

### F4 — Shared board with member filter

- Show all chores on one shared board.
- Show each chore's title, assigned member, and status.
- Pending and completed chores must be distinguishable.
- Allow the board to be optionally filtered by household member.
- No separate dashboards, search, sorting controls, pagination, or advanced filters.

## 5. User Flows

1. **Adding a household member:** The user adds a member by name. The member becomes a saved household member and is available for future chore assignment.
2. **Creating and assigning a chore:** The user creates a chore by entering a title and assigning it to exactly one existing household member. The chore is added to the shared board as pending.
3. **Viewing the shared board:** The user sees all chores, each showing its title, assigned member, and status. Pending and completed chores are visually distinguishable.
4. **Filtering chores by household member:** The user optionally restricts the board to show only the chores assigned to one selected member.
5. **Marking a pending chore completed:** The user marks a pending chore completed with one Done action. Its status changes from pending to completed.

## 6. Acceptance Criteria

- AC1: A household member can be added by name, and that name becomes available for selection when assigning chores.
- AC2: A chore can be created with a title and assigned to exactly one existing household member during creation.
- AC3: A newly created chore appears on the shared board with its title and assigned member, and its status is pending.
- AC4: The shared board shows all chores, and pending and completed chores are distinguishable.
- AC5: A pending chore can be marked completed with one Done action, after which its status is completed.
- AC6: The board can be filtered to show only chores assigned to a selected household member.
- AC7: The application does not enforce who performs an action (no authentication or current-user concept).

## 7. Non-Goals

- authentication/accounts/passwords
- multiple households
- roles/permissions
- recurring chores
- scheduling
- reminders/notifications
- claiming/reassignment
- editing/deleting chores
- completion approval
- reopening completed chores
- search/sorting/pagination
- separate mobile clients

## 8. Definition of Done

The application is done when all of the following hold:

- F1 is implemented: members can be added by name and selected for assignment (AC1).
- F2 is implemented: chores can be created with a title and assigned to exactly one existing member (AC2, AC3).
- F3 is implemented: chores start pending, can be marked completed with one Done action, and the application does not enforce who performs the action (AC5, AC7).
- F4 is implemented: the shared board shows all chores with title, member, and distinguishable status, and supports filtering by member (AC4, AC6).
- All acceptance criteria AC1–AC7 pass.
- Nothing outside the approved features and non-goals is implemented.