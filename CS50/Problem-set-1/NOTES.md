# Conditionals — Interview Recall Sheet

Part 1 is syntax you should be able to write cold. Part 2 is questions with the answer phrased the way you'd **say it out loud** — read the question, answer from memory, check. Definitions marked *(docs)* are quoted from docs.python.org, so you can say them verbatim.

---

## Part 1 — Syntax

**The `if` statement**
```python
if score >= 90:
    grade = "A"
elif score >= 80:          # zero or more elif, checked in order
    grade = "B"
else:                      # at most one else, optional
    grade = "F"
```

**Comparison operators**
```python
x == y    x != y           # equality / inequality
x < y     x <= y           # ordering
x > y     x >= y
x is y    x is not y       # same object, not same value
x in seq  x not in seq     # membership
```

**Chaining** — write the range the way you'd say it:
```python
if 7 <= time <= 8:         # one expression, time evaluated once
if 0 < n < 10 < m:         # chains as long as you like
```

**Boolean operators** — lowest precedence, so comparisons bind tighter:
```python
if age >= 18 and has_id:
if day == "sat" or day == "sun":
if not logged_in:
if x in ("sat", "sun"):    # better than a chain of == for one variable
```

**Conditional expression** (the ternary) — an expression, so it has a value:
```python
label = "even" if n % 2 == 0 else "odd"
```

**Truthiness** — test the object, not its length:
```python
if items:          # not: if len(items) > 0
if not name:       # not: if name == ""
if x is None:      # None is compared with `is`, never ==
```

**`match`** (Python 3.10+) — for dispatching one value over many literals:
```python
match operator:
    case "+":
        return x + z
    case "-" | "*":        # | is "or" inside a pattern
        return "dash or star"
    case _:                # _ is the wildcard, like else
        return None
```

**String predicates that return a bool** — the whole vocabulary of Problem Set 1:
```python
s.startswith("hello")     s.endswith(".png")
s.startswith(("a", "b"))  # a tuple means "any of these"
"42" in s                 # substring test
s.lower()   s.upper()     s.strip()      # normalise BEFORE comparing
s.split(":")              # "7:30" -> ["7", "30"]
```

**`in` on different types**
```python
"ab" in "cab"        # substring
3 in [1, 2, 3]       # element
"k" in {"k": 1}      # KEY, not value
```

**Guard clause** — return early instead of nesting:
```python
def fine(greeting):
    if greeting.startswith("hello"):
        return "$0"
    if greeting.startswith("h"):
        return "$20"
    return "$100"
```

---

## Part 2 — Recall cards

### 1. What does `if` actually take?
Any expression, not just a comparison. Python evaluates it and applies **truth testing** to the result, so `if items:` and `if n:` are valid and idiomatic. The clause runs when the value is truthy.

### 2. What's falsy in Python?
`None`, `False`, zero of any numeric type, and every empty sequence or mapping — `""`, `[]`, `{}`, `()`, `set()`, `range(0)`. Everything else is truthy, including `"0"`, `"False"`, and `[0]`.

### 3. `if`, `elif`, `else` vs three separate `if`s?
A single `if/elif/else` chain picks **exactly one** branch: the first true test wins and the rest are never evaluated. Three separate `if`s are three independent tests, so two can fire. If the conditions overlap — `startswith("hello")` and `startswith("h")` — separate `if`s are a bug and `elif` is the fix.

### 4. Does branch order matter?
Yes, when the conditions overlap. `startswith("h")` is true for every `"hello"`, so the specific test must come first; put it second and `"hello"` can never reach `"$0"`. Rule of thumb: **most specific condition first.**

### 5. `==` vs `is`?
`==` asks "do these have the same value" and calls the object's `__eq__`. `is` asks "are these the *same object* in memory." `[1, 2] == [1, 2]` is `True` but `[1, 2] is [1, 2]` is `False`. Use `is` only for singletons — `None`, `True`, `False` — and `==` for everything else.

### 6. How do you test for `None`?
`if x is None:` There is exactly one `None` object, so identity is the correct and fastest test. `x == None` can be overridden by a class, and `if not x:` is wrong because it also catches `0`, `""`, and `[]` — which is the difference between "no value given" and "the value given was zero."

### 7. Why does `7 <= time <= 8` work?
Python supports **chained comparison**: it's shorthand for `7 <= time and time <= 8`, except `time` is evaluated only once. Most languages parse `7 <= time <= 8` as `(7 <= time) <= 8` and compare a bool to a number; Python doesn't.

### 8. `if day == "sat" or "sun":` — what's wrong?
It's always true. `or` binds looser than `==`, so this reads `(day == "sat") or ("sun")` and `"sun"` is a non-empty string, hence truthy. Write `day in ("sat", "sun")`.

### 9. What is short-circuit evaluation?
`and` stops at the first falsy operand and `or` stops at the first truthy one, and neither evaluates what's left. That's what makes `if n != 0 and total / n > 1:` safe — the division never runs when `n` is `0`. Order the cheap or protective test first.

### 10. What do `and` and `or` return?
**An operand, not a bool.** `and` returns the first falsy operand or the last one; `or` returns the first truthy operand or the last one. So `3 and 0` is `0` and `0 or "x"` is `"x"` — which is why `name = name or "anonymous"` is a common default idiom. `not` is the exception: it always returns a real `True` or `False`.

### 11. Is `True` a number?
Yes. `bool` is a subclass of `int`, with `True == 1` and `False == 0`, so `True + True` is `2` and `sum([True, False, True])` counts the trues. Handy, but don't rely on it in code someone else has to read.

### 12. Precedence to actually remember?
Arithmetic, then comparisons, then `not`, then `and`, then `or`. So `a == 1 or b == 2 and c == 3` is `a == 1 or (b == 2 and c == 3)`. When a condition needs a reader to recall this table, add the parentheses.

### 13. `if/elif` chain vs `match`?
Use `match` when you're dispatching **one value over many literal alternatives** — an operator, a command, a file extension — because the intent is flatter and `case "a" | "b":` groups alternatives. Use `if/elif` when the branches test different things, call methods like `startswith`, or compare ranges. `match` is Python 3.10+ and does structural pattern matching, not a C-style fall-through switch; there's no `break` and no fall-through.

### 14. What's the `_` in `case _:`?
The **wildcard pattern** — it matches anything and is the `match` equivalent of `else`. Without it, a `match` with no matching case simply does nothing and falls through, which is a quiet source of `None` returns.

### 15. Why normalise input before comparing?
Comparison is exact: `"Hello" == "hello"` is `False`, and `" hello "` starts with a space, not an `h`. So `s.lower().strip()` once, up front, collapses case and stray whitespace and shrinks the number of branches you need. Note that string methods **return a new string** — `s.lower()` on its own line does nothing, you must assign it.

### 16. `startswith` vs slicing?
`s.startswith("hello")` is clearer, can't go out of range, and takes a tuple for "any of these": `s.startswith(("a", "b"))`. `s[:5] == "hello"` does the same thing but repeats the magic number `5` and silently compares a short string against it.

### 17. What does `in` test on a dict?
**Keys only.** `"k" in d` checks the keys; to search values you need `v in d.values()`. Key lookup is O(1) via hashing, while scanning values is O(n).

### 18. What does `return` do to a conditional?
It exits the function immediately, so a `return` in an `if` makes the following `elif`/`else` redundant — which is the **guard clause** style: a flat series of `if ...: return ...` ending in an unconditional `return` for the fallback. Flatter than nesting, and each case reads as one line.

### 19. Why does `is_valid()` return a bool instead of printing?
So the caller decides what to do with the answer. A predicate that returns `True`/`False` can be used in an `if`, negated, combined with `and`, and unit-tested; one that prints `"Valid"` can only ever print. **Name predicates `is_`/`has_`/`can_` and have them return a bool.**

### 20. Can you write `if x = 5:`?
No — `SyntaxError`. Assignment is a **statement**, not an expression, so Python structurally prevents the C typo of `=` for `==`. If you genuinely want to assign inside a condition, that's the walrus operator: `if (n := len(s)) > 6:`.

### 21. Is `else` ever optional?
Always. `if` alone is legal, and `elif` is optional too. But a function whose branches all `return` and which has **no final fallback** returns `None` when nothing matches — that's how a bad input turns into a `TypeError` three lines later. Either end with an unconditional `return` or make the missing case explicit.

### 22. How do you validate input that might not be a number?
Catch the exception rather than testing first, because `int()` is the only thing that really knows:
```python
try:
    n = int(input("n: "))
except ValueError:
    print("Not a number")
```
`"3.7".isdigit()` is `False` and `"-5".isdigit()` is `False` too, so `isdigit()` is not an integer test.

### 23. Why compare `float` results with care?
`0.1 + 0.2 == 0.3` is `False`, because floats are binary approximations. So `if total == 0.3:` can fail on arithmetic that's mathematically right. Compare with a tolerance (`math.isclose`), or keep money in integer cents or `decimal.Decimal`.

---

## The spine — if you remember ten lines

1. `if` takes any expression and truth-tests the result, so `if items:` is the idiom.
2. Falsy: `None`, `False`, any zero, any empty container. Everything else is truthy.
3. An `if/elif/else` chain runs exactly one branch; separate `if`s run independently.
4. When conditions overlap, order decides — most specific first.
5. `==` is same value, `is` is same object; use `is` only for `None`, `True`, `False`.
6. `7 <= t <= 8` chains, and evaluates `t` once.
7. `and`/`or` short-circuit and return an operand, not a bool.
8. `or` binds looser than `==`, so `day == "sat" or "sun"` is always true.
9. `in` on a dict tests keys, not values.
10. Normalise with `.lower().strip()` before comparing, and assign the result.
