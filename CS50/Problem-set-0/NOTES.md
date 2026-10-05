# Python Foundations — Notes from Problem Set 0

Written against my own solutions in this folder (`indoor`, `playback`, `faces`, `einstein`, `tip`).
Every rule below is tied to a line I actually wrote, so revising this should replay the reasoning, not just the vocabulary.

---

## 1. The one mental model everything else hangs off

In Python, a **variable is a name bound to an object**. The name is not a box that holds a value; it is a label pointing at a value that lives somewhere in memory. Assignment (`=`) does exactly one thing: it points a name at an object.

```python
userInput = input("Enter a message/string: ")
```

Here `input(...)` produces a string object, and the name `userInput` is made to point at it. Nothing is "copied into" `userInput`.

Three consequences follow immediately, and they explain most beginner surprises:

1. A name has no type; the **object** has a type. `x = 5` then `x = "five"` is legal, because the second assignment just re-points the label.
2. Rebinding a name never modifies the old object. It only stops pointing at it.
3. Two names can point at the same object, so "changing the object" and "changing the name" are different events. This is the root of the mutability questions in §11.

---

## 2. Variables

**No declaration step.** A variable comes into existence the moment it is first assigned. There is no `int x;`. Reading a name that was never assigned raises `NameError`.

**Dynamic typing, not weak typing.** Python will not quietly reinterpret types for you. `"5" + 5` is a `TypeError`, not `"55"` or `10`. The type lives with the value and is enforced at runtime.

**Assignment is a statement, not an expression.** `tip = dollars * percent` evaluates the right side completely, then binds the name. The right side cannot see the new value of the left side mid-statement.

**Reassignment using the old value is ordinary.** In `faces.py`:

```python
userInput = userInput.replace(":)", "🙂")
```

The right side is evaluated first (producing a brand-new string), and only then is `userInput` re-pointed at that new string. The original string object is unchanged and simply becomes unreachable.

**Naming.** PEP 8, the Python style guide, specifies `snake_case` for variables and functions. My `takeInput`, `toLowerCase`, and `slowingDown` are `camelCase`, which is Java/JavaScript convention and reads as non-idiomatic to a Python reviewer; `tip.py` gets this right with `dollars_to_float` and `percent_to_float`. Worth fixing habitually now, because style is the cheapest signal of fluency in an interview.

**Constants** are a convention only. In `einstein.py` I wrote `c = 300000000`; idiomatically that would be `C = 300_000_000` — uppercase to signal "do not reassign", and underscores as digit separators for readability. Python does not enforce immutability for it.

---

## 3. `input()` always returns a string

`input()` prints its optional prompt argument, reads one line from standard input, strips the trailing newline, and **returns a `str`** — always, with no exceptions. If the user types `100`, you get the two-character string `"100"`, not the integer.

This is why `einstein.py` cannot do arithmetic on the raw input:

```python
mass = int(input("Enter mass: "))   # str -> int before multiplying
```

The functions `int()`, `float()`, and `str()` are **conversions**, not casts: each constructs a new object of that type from the old one. `int("100")` returns a new integer; the string is untouched.

Conversion rules worth knowing precisely:

- `int("100")` works. `int("100.5")` raises `ValueError` — `int()` will not parse a decimal point out of a string.
- `int(100.9)` returns `100`. Converting a float to an int **truncates toward zero**; it does not round. `int(-100.9)` is `-100`.
- `float("100")` works and gives `100.0`. `float("abc")` raises `ValueError`.

---

## 4. Functions: definition versus call

```python
def takeInput():
    userInput = input("Enter a message/string: ")
    return userInput
```

`def` is a statement that **executes at import/run time** and does one thing: it creates a function object and binds it to the name `takeInput`. The body is compiled but not run. The body only runs when the function is **called**, i.e. when the name is followed by parentheses: `takeInput()`.

That distinction matters concretely:

- `takeInput` is the function object itself. You can pass it around, store it in a list, or hand it to another function.
- `takeInput()` is a *call expression*; it runs the body and evaluates to whatever the body returns.

Writing `print(takeInput)` would print something like `<function takeInput at 0x104f2e8e0>`, which is the classic symptom of a forgotten pair of parentheses.

**Why bother with functions at all** — three reasons, in order of how often they come up:

1. **Decomposition.** Each function names one step, so `main()` reads as a summary of the program rather than a wall of operations.
2. **Reuse.** `dollars_to_float` and `percent_to_float` in `tip.py` are nearly the same shape, which makes the duplication visible and therefore fixable.
3. **Testability.** A function that takes an argument and returns a value can be tested with a single line. A function that reads from `input()` and writes to `print()` can only be tested by driving a whole program, which is exactly the problem described in §7.

---

## 5. Parameters versus arguments

These are two sides of the same handoff, and interviewers do ask for the distinction:

- A **parameter** is the name in the function definition — the local variable the function promises to have. `mass` in `def calculateEnergy(mass):`.
- An **argument** is the actual value supplied at the call site. The value of `mass` in `energy = calculateEnergy(mass)`.

The two happen to share the spelling `mass` in my `einstein.py`, which is coincidence, not connection. The caller's `mass` lives in `main`'s scope; the parameter `mass` is a separate local name inside `calculateEnergy`. I could rename either one without touching the other.

**Calling by position versus by keyword.** `calculateEnergy(5)` passes positionally. `calculateEnergy(mass=5)` passes by keyword, which is self-documenting and order-independent. Positional arguments must come before keyword arguments in a call.

**Default values** let a parameter be optional: `def greet(name, greeting="Hello"):`. The default is evaluated **once, when the `def` runs** — not on each call. That is why a mutable default like `def f(items=[])` is a well-known bug: every call shares the same list. The standard fix is `def f(items=None)` and then `if items is None: items = []`.

**Arity is checked at call time.** Calling `calculateEnergy()` with no argument raises `TypeError: calculateEnergy() missing 1 required positional argument: 'mass'`.

---

## 6. How arguments are passed (the "pass by value or reference?" question)

Neither, strictly. Python passes **the object reference, by value**: the parameter becomes a new local name pointing at the *same* object the caller passed. The usual name for this is "pass by assignment" or "pass by object reference".

The practical rule that falls out of it:

- **Rebinding a parameter never affects the caller.** Inside `convert`, the line `userInput = userInput.replace(...)` re-points the *local* name only. `main`'s `inp` still points at the original string. This is precisely why `convert` has to `return` the result — otherwise the work is thrown away when the function exits.
- **Mutating the object the parameter points at *does* affect the caller**, because both names point at the same object. `def add(lst): lst.append(1)` is visible to the caller.

Strings cannot be mutated at all (§11), so with `str`, `int`, and `float` arguments only the first case is ever possible — and `return` is therefore the only way to get a result out.

---

## 7. `return` versus `print` — the most important distinction in this problem set

These do completely unrelated things, and my own five files are split across both styles, which makes the comparison easy.

**`return` hands a value back to the caller** and ends the function immediately. The value becomes the result of the call expression, so the caller can store it, pass it on, or compare it. Nothing is displayed.

**`print` writes text to standard output** for a human to read. It returns `None`. The value is gone as far as the program is concerned — nothing can catch it.

Compare what I wrote:

```python
# faces.py — convert returns, main decides what to do with it
def convert(userInput):
    userInput = userInput.replace(":)", "🙂")
    return userInput

# indoor.py — toLowerCase prints and returns nothing
def toLowerCase(userInput):
    lower_case_string = userInput.lower()
    print(lower_case_string)
```

`convert` is the better design, and the reason is reusability: I can write `print(convert(s))`, or `convert(s).upper()`, or `assert convert(":)") == "🙂"`. With `toLowerCase` I can do exactly one thing — cause output — and I cannot test it without capturing stdout. A function that both computes and prints has fused a decision (*where does this go?*) into a calculation that should not care.

The habit to keep: **compute and return in the helpers; print at the edge, usually in `main`.**

**Implicit return.** A function that ends without a `return`, or hits a bare `return`, returns `None`. So `toLowerCase` *does* return a value: `None`. This is why `x = toLowerCase("ABC")` leaves `x` as `None` — a silent bug class, since `None` only blows up later, somewhere else.

**`return` exits immediately.** Any code after it in the same block never runs, which makes `return` useful as an early exit for guard clauses, not just as a final step.

**Returning multiple values** is really returning one tuple: `return a, b` builds `(a, b)`, and `x, y = f()` unpacks it.

---

## 8. Scope

A name assigned inside a function is **local** to that call. It is created when the call starts and destroyed when the call ends. `lower_case_string` inside `toLowerCase` does not exist anywhere else, and a second call creates a fresh one.

Python resolves names by the **LEGB** rule, in order: **L**ocal, then **E**nclosing (enclosing functions), then **G**lobal (module level), then **B**uilt-in (`print`, `input`, `int`, …). The first match wins, which is why naming a variable `input` or `list` shadows the builtin for the rest of that scope and causes confusing failures later.

Reading a global from inside a function works. **Assigning** to that name inside the function instead creates a new local, unless declared `global` — and needing `global` is almost always a sign the value should have been a parameter and a return value instead.

Function *definitions* at module level are global, which is why `main()` can call `takeInput` even though `takeInput` is defined above it in the file. What actually matters is that the `def` has executed **before the call runs**, not before the call is written. This is the subtlety in `tip.py`: `main()` is defined first and calls `dollars_to_float`, which is defined further down. That works because the final line `main()` executes only after the whole module — all three `def`s — has been run top to bottom.

---

## 9. The `main()` pattern

```python
def main():
    ...
main()
```

Wrapping the top-level logic in `main()` keeps the module's only side effect at the bottom in one obvious place, and keeps working variables out of the global scope. `indoor.py` and `playback.py` skip this and run statements directly at module level, which works but scatters the entry point.

The idiomatic form adds a guard:

```python
if __name__ == "__main__":
    main()
```

`__name__` is a module-level string Python sets automatically: it is `"__main__"` when the file is run directly (`python tip.py`), and the module's own name (`"tip"`) when the file is **imported** by something else. So the guard means "run this only when executed as a script". Without it, a bare `main()` fires on import, which means importing `tip.py` to test `dollars_to_float` would immediately block on `input()`. CS50's `check50` imports your module in several checks, so this is practical and not just ceremony.

---

## 10. Strings are immutable

A `str` object can never be changed in place. Every string "modification" returns a **new** string and leaves the original untouched. There is no `s[0] = "x"`; that raises `TypeError`.

This is the single fact that explains the shape of `faces.py`:

```python
userInput.replace(":)", "🙂")          # computes a new string, discards it
userInput = userInput.replace(":)", "🙂")  # computes it and keeps it
```

The first line is a complete, legal, entirely useless statement. Forgetting the reassignment is the most common string bug there is, and it fails silently rather than erroring.

The same reasoning applies to `.lower()` in `indoor.py` and `.replace(" ", "...")` in `playback.py`: both are non-destructive and both return a value that must be captured or used.

**Methods versus functions.** `userInput.replace(...)` is a *method* — a function that belongs to the string object and receives it implicitly as its first argument. `len(userInput)` is a plain *function* that takes the string explicitly. Methods are reached through the dot operator on a value; functions stand alone.

**Chaining** works because each method returns a new string, which has methods of its own: `s.replace(":)", "🙂").replace(":(", "🙁")` does both substitutions in one expression, and would compress `convert` to a single line.

The string methods used in this problem set, precisely:

- `.lower()` — returns a lowercased copy. `.upper()` is its mirror.
- `.replace(old, new)` — returns a copy with **every** non-overlapping occurrence of `old` replaced. Not just the first. `.replace(old, new, 1)` limits it to one.
- `.strip()` — returns a copy with leading and trailing whitespace removed. Not used above, but the standard defence against a user typing a stray space.

---

## 11. f-strings and format specifiers

```python
print(f"Leave ${tip:.2f}")
```

The `f` prefix makes this a **formatted string literal**: expressions inside `{}` are evaluated at runtime and their results inserted. The part after the colon is a **format specification**, not part of the value. `.2f` means "render as a fixed-point decimal with exactly two digits after the point", which is what makes `3.5` display as `3.50` and `3.456` as `3.46`.

Two points that matter:

- Formatting is **display-only**. `tip` itself is still the full-precision float; `.2f` changes nothing about the stored number.
- `.2f` **rounds** for display, while `int()` truncates. Don't conflate them.

The first `$` is a literal dollar sign in the text; the braces are what Python interprets. To print a literal brace, double it: `{{`.

---

## 12. Numbers and arithmetic

`einstein.py` relies on two things being read correctly:

```python
e = mass * c**2
```

**Precedence**: `**` (exponentiation) binds tighter than `*`, so this is `mass * (c ** 2)`, which is what E = mc² requires. `(mass * c) ** 2` would be a different and wrong answer. `**` is also **right**-associative: `2**3**2` is `2**(3**2)` = 512, not 64.

**int versus float**: `int` is an arbitrary-precision integer in Python — it does not overflow, so `mass * c**2` with a large `c` is exact. `float` is a 64-bit IEEE 754 double, so it carries roughly 15–17 significant digits and cannot represent most decimals exactly. `0.1 + 0.2 == 0.3` is `False`. This is why money is formatted with `.2f` for output, and why real financial code uses `decimal.Decimal` rather than `float`.

**Division**: `/` always produces a `float` (`4 / 2` is `2.0`), `//` is floor division, and `%` is the remainder. `percent_to_float` returns `float(p)/100` — already a float, so the `/` is harmless, but note the deliberate conversion to a fraction so the caller can simply multiply.

---

## 13. Errors, and the difference between a crash and a bug

Python signals runtime problems by **raising exceptions**, which propagate up and terminate the program with a traceback unless caught. The two that appear here:

- `ValueError` — the type was right but the value was not convertible: `int("abc")`, `float("12%")`.
- `TypeError` — the type itself was wrong for the operation: `"5" + 5`, or a call with the wrong number of arguments.

`tip.py` originally crashed when the input omitted the `$` or `%`, because it sliced characters off positionally instead of removing them; `.replace("$", "")` is robust precisely because it is a no-op when the character is absent. That is the general lesson: prefer operations whose behaviour on the *unexpected* input is still sensible.

Validation, when it is needed, uses `try`/`except` around the conversion:

```python
try:
    mass = int(input("Enter mass: "))
except ValueError:
    print("Not a number")
```

The guiding distinction: a **crash** is loud and tells you exactly where it happened; a **silent bug** — a discarded `.replace()`, a function that prints instead of returning, a `None` flowing where a number belongs — is the expensive kind. Designing with return values makes more of your mistakes the loud kind.

---

## 14. What I would change in my own five files

Worth re-reading as a review checklist, because each item maps to a concept above:

1. `indoor.py` and `playback.py` print inside their helper. They should return the transformed string and let the caller print it (§7).
2. Both also lack a `main()`, so module-level code is doing the orchestrating (§9).
3. All five would be better with `if __name__ == "__main__": main()` instead of a bare `main()` (§9).
4. `takeInput()` adds nothing: it wraps a single `input()` call and returns it unchanged. A function should earn its name by doing something; `input(...)` inline is clearer.
5. `camelCase` names should be `snake_case` (§2).
6. `c = 300000000` should be `C = 300_000_000` (§2).
7. `convert` in `faces.py` can chain its two `.replace()` calls into one expression (§10).

---

## Conceptual questions

Answer these out loud before reading §Answers. They are ordered roughly by how likely each is to come up in an interview.

**Variables and objects**
1. What exactly does `x = 5` do, in terms of names and objects?
2. Is Python dynamically typed, weakly typed, both, or neither? Justify it with an expression that fails.
3. `a = "hi"` then `b = a` then `a = "bye"`. What is `b`, and why?
4. What is the difference between a variable's type and a name's type?

**Functions**
5. What is the difference between `takeInput` and `takeInput()`?
6. When does the body of a function execute relative to its `def` statement?
7. Distinguish a parameter from an argument using `calculateEnergy(mass)`.
8. Why is `def f(items=[])` considered a bug, and what is the fix?
9. `tip.py` defines `main()` before `dollars_to_float` but calls it from inside `main`. Why does that work?

**Return values**
10. What does `toLowerCase` in `indoor.py` return?
11. Give two concrete things you can do with `convert()` from `faces.py` that you cannot do with `toLowerCase()` from `indoor.py`.
12. What happens to code written after a `return` statement in the same block?
13. How does a function return two values?

**Argument passing and mutability**
14. Is Python pass-by-value or pass-by-reference? Defend your answer.
15. Inside `convert`, `userInput = userInput.replace(...)` reassigns the parameter. Why does the caller's variable stay unchanged?
16. If the parameter were a list and you called `.append()` on it, would the caller see the change? Why is that different from question 15?

**Strings**
17. What is wrong with the statement `userInput.replace(":)", "🙂")` on a line of its own?
18. Does `.replace()` replace the first occurrence or all of them?
19. What is the difference between a method and a function, in terms of how each receives the string it operates on?

**Input and types**
20. What type does `input()` return when the user types `42`?
21. Why does `int("100.5")` fail while `int(100.5)` succeeds? What is the value of the second?
22. What is the difference between `int(-3.7)` and `round(-3.7)`?

**Numbers and formatting**
23. Does `mass * c**2` compute `mass * (c**2)` or `(mass * c)**2`? What rule decides?
24. In `f"{tip:.2f}"`, does `.2f` change the value of `tip`?
25. Why is `0.1 + 0.2 == 0.3` false, and what would you use instead for money?

**Program structure**
26. What is `__name__` equal to when a file is run directly, versus imported?
27. Name one concrete problem caused by calling `main()` without the `__name__` guard.
28. Why does a function that both computes a value and prints it make testing harder?

---

## Answers

1. It creates (or reuses) the integer object `5` and binds the name `x` to it. The name is a label, not a container.
2. Dynamically typed but **strongly** typed: types are checked at runtime, and Python refuses silent coercion — `"5" + 5` raises `TypeError` rather than guessing.
3. `b` is still `"hi"`. `b = a` copied the reference to the string `"hi"`; rebinding `a` only moved `a`'s label and did not touch `b` or the object.
4. Names have no type at all; only objects do. The same name can be bound to objects of different types over its lifetime.
5. `takeInput` evaluates to the function object itself and can be passed around; `takeInput()` calls it, runs the body, and evaluates to the returned value.
6. The `def` executes immediately and only binds a name to a function object. The body executes later, once per call.
7. `mass` in the `def` line is the parameter — a local name the function will have. The `mass` passed at the call site is the argument — the actual value. They are independent names that happen to share a spelling.
8. The default is evaluated once when the `def` runs, so every call shares one list and mutations accumulate across calls. Use `items=None` and build a fresh list inside the function.
9. Because name lookup happens when the call *runs*, not when it is written. By the time the final `main()` line executes, the whole module has run and all three `def`s have bound their names.
10. `None`. It has no `return` statement, so it returns `None` implicitly; its visible effect is output, not a value.
11. Store or transform the result (`x = convert(s)`, `convert(s).upper()`), and assert on it in a test (`assert convert(":)") == "🙂"`). `toLowerCase` only produces output, which you would have to capture from stdout.
12. It never executes. `return` exits the function immediately.
13. By returning a tuple — `return a, b` builds `(a, b)`, which the caller can unpack with `x, y = f()`.
14. Neither, exactly: it passes the object reference by value, often called pass-by-assignment. The parameter is a new local name bound to the same object the caller passed.
15. Because assignment rebinds the local name only. It changes which object the local `userInput` points at and leaves the caller's binding, and the original object, untouched.
16. Yes, the caller would see it, because `.append()` mutates the shared object rather than rebinding a name. Question 15 was a rebinding; this is a mutation. Strings cannot be mutated, so only rebinding is possible with them.
17. It computes a new string and immediately discards it. Strings are immutable, so the original is unchanged — the line is legal and has no effect, which makes it a silent bug.
18. All non-overlapping occurrences, unless you pass a count as the third argument.
19. A method is accessed through the object with the dot operator and receives that object implicitly as its first argument; a plain function receives it explicitly as a normal argument, like `len(s)`.
20. `str` — the two-character string `"42"`. `input()` never returns a number.
21. `int()` parsing a *string* accepts only an integer literal, so the decimal point raises `ValueError`; given a *float* it truncates toward zero instead, yielding `100`.
22. `int(-3.7)` truncates toward zero, giving `-3`. `round(-3.7)` rounds to nearest, giving `-4`.
23. `mass * (c**2)`, because `**` has higher precedence than `*`. That is what E = mc² requires.
24. No. Format specifications affect only the rendered text; `tip` keeps its full float precision.
25. Because binary floating point cannot represent `0.1`, `0.2`, or `0.3` exactly, so the sum is very slightly off. For money, use `decimal.Decimal`, or work in integer cents.
26. `"__main__"` when run directly; the module's own name (e.g. `"tip"`) when imported.
27. Importing the module — which `check50` does, and which any test would do — immediately runs the program and blocks on `input()`, so the helpers can never be tested in isolation.
28. The function fuses a calculation with a decision about where output goes. To check the calculation you must capture standard output and parse text, instead of comparing a returned value to an expected one.
