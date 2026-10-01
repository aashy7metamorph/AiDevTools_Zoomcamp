# AGENTS.md

## Project

- Small Django learning project for managing shared household chores.
- `_docs/plan.md` is the source of truth for product scope and acceptance criteria.

## Agent Rules

- Read `_docs/plan.md` before implementing product behavior.
- Implement only the currently assigned backlog task.
- Do not add features outside the approved scope.
- Do not invent requirements when something is unclear.
- Avoid unrelated refactoring.
- Keep changes small and focused.
- Inspect existing code before editing.
- Preserve already-working behavior.

## Testing

Before claiming a task is complete:

- run the relevant tests
- verify the behavior manually when appropriate
- report what was tested
- report any failures or unresolved issues

## Completion Report

After every implementation task, report:

- task completed
- files changed
- tests/commands run
- result
- any remaining concerns