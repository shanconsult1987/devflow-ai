---
name: python-quality
description: Use when developing, testing, debugging or reviewing Python code.
---

# Python Quality Engineering

## Inspection

Read the relevant source files and tests.

Understand existing behaviour before changes.

## Implementation

- Use type hints.
- Validate inputs.
- Keep functions focused.
- Avoid unnecessary dependencies.
- Preserve existing behaviour.

## Testing

Test:

- Normal values.
- Invalid values.
- Empty values.
- Boundary conditions.
- Regression scenarios.

## Execution

Run:

python -m pytest -v

Do not report success without execution.

## Review

Check correctness, security, maintainability
and error handling.

## Completion

Report files changed, test evidence and risks.