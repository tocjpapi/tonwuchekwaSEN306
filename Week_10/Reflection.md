# Reflection 

## Issues in HandleStuff

Going through the routine, I found these problems:

1. **Bad name** — `HandleStuff` tells you nothing about what it actually does.
2. **No documentation** — no docstring or explanation of what parameters are expected.
3. **Inconsistent layout** — the `expenseType == 1` branch has a loop but `== 2` and `== 3` don't, and the indentation style changes randomly.
4. **Input variable mutated** — `inputRec` sounds like input-only but gets modified inside the function.
5. **Uses global variables** — reads `corpExpense` and writes to `profit` without those being parameters, which makes the function hard to test or reuse.
6. **No single purpose** — it initialises data, calls a database function, calculates revenue, and updates colours all in one place. That's at least four different jobs.
7. **No input validation** — if `crntQtr` is 0, the revenue line crashes with a division by zero error.
8. **Magic numbers** — `100`, `4.0`, `12`, `2`, `3` appear with no explanation of what they represent.
9. **Unused parameters** — `screenX` and `screenY` are never used inside the function.
10. **Output parameter never assigned** — `prevColor` is passed as a reference in C++ (suggesting it should be set), but it never is.
11. **Too many parameters** — 11 is way over the recommended max of 7.
12. **Parameters poorly ordered and not documented** — they're not arranged input → modify → output and none have type hints or descriptions.

## What I Applied in CustomerRefactored.py

I split the logic into small functions that each do one thing — validation, discount calculation, totalling, and printing are all separate. I used dataclasses to group related data so no function needs more than two parameters, replaced all magic numbers with named constants, and made sure every function returns a value instead of modifying globals.

The biggest takeaway is that naming is harder than it looks — if you can't give a function a clear name, it's usually a sign the function is doing too much.