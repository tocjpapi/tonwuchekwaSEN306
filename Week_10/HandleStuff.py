# ============================================================
# HandleStuff.py
# SEN306 Lecture 8 - High Quality Routines
#
# This is the LOW-QUALITY routine shown in slides 11.
# It intentionally preserves ALL the original bugs and
# bad practices identified in slides 12-15.
# ============================================================

# Simulated globals (bad practice — see Issue 6)
corpExpense = [[i * 0.5 for i in range(100)] for _ in range(5)]
profit = [0.0] * 100
revenue = [500.0 + i for i in range(100)]


def HandleStuff(inputRec, crntQtr, empRec,
                estimRevenue, ytdRevenue, screenX, screenY,
                newColor, prevColor, status, expenseType):
    # Issue 1:  Bad name — "HandleStuff" says nothing about purpose
    # Issue 2:  No documentation / docstring
    # Issue 3:  Bad layout — inconsistent indentation and style
    # Issue 4:  inputRec is labelled as input but is being modified (Issue 5)
    # Issue 5:  inputRec (input variable) is mutated inside the routine
    # Issue 6:  Reads global corpExpense, writes to global profit
    # Issue 7:  Does NOT have a single purpose (init + DB update + calc)
    # Issue 8:  No guard against crntQtr == 0 → ZeroDivisionError
    # Issue 9:  Magic numbers: 100, 4.0, 12, 2, 3
    # Issue 10: screenX and screenY are never used
    # Issue 11: prevColor is never assigned a value (passed but unused as output)
    # Issue 12: Too many parameters (11); poorly ordered; none documented

    i = 0
    for i in range(100):                           # magic number 100
        inputRec['revenue'][i] = 0                 # mutates input variable
        inputRec['expense'][i] = corpExpense[crntQtr][i]  # reads global

    UpdateCorpDatabase(empRec)                     # side effect — DB write

    estimRevenue = ytdRevenue * 4.0 / crntQtr      # magic 4.0; div-by-zero risk

    newColor = prevColor                           # prevColor never set here
    status = 'SUCCESS'                             # magic string

    if expenseType == 1:                           # magic number 1
        for i in range(12):                        # magic number 12
            profit[i] = revenue[i] - inputRec['expense'][i]   # writes global profit

    elif expenseType == 2:                         # magic number 2; no loop!
            profit[i] = revenue[i] - inputRec['expense'][i]   # Bug preserved: no loop

    elif expenseType == 3:                         # magic number 3; no loop!
            profit[i] = revenue[i] - inputRec['expense'][i]   # Bug preserved: no loop


def UpdateCorpDatabase(empRec):
    """Stub representing a database update call."""
    pass


# ── Quick demo ────────────────────────────────────────────────
if __name__ == '__main__':
    rec = {'revenue': [0.0] * 100, 'expense': [0.0] * 100}
    HandleStuff(rec, 1, 'emp001',
                0, 1200.0, 0, 0,
                'blue', 'red', 'PENDING', 1)
    print("HandleStuff ran (with all its flaws intact).")