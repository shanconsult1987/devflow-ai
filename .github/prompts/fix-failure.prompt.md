---
name: fix-failure
description: Diagnose and fix an implementation or test failure.
---

Investigate the following failure:

${input:failure:Test failure or GitHub Actions failure}

Steps:

1. Retrieve the actual failure.
2. Identify the failing file and line.
3. Understand the root cause.
4. Identify the affected requirement.
5. Propose a minimal correction.
6. Implement the correction.
7. Add a regression test.
8. Execute all tests.
9. Report the result.

Do not disable tests.
Do not weaken assertions merely to pass.
Do not hide errors.
Do not merge changes.