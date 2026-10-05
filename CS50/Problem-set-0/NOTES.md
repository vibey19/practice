# Python Basics — Interview Recall Sheet

Part 1 is syntax you should be able to write cold. Part 2 is questions with the answer phrased the way you'd **say it out loud** — read the question, answer from memory, check. Definitions marked *(docs)* are quoted from docs.python.org, so you can say them verbatim.

---

## Part 1 — Syntax

**Variables**
```python
x = 5                  # bind the name x to the object 5
x, y = 1, 2            # tuple unpacking
x, y = y, x            # swap, no temp variable
x = y = 0              # chained assignment, both names -> same object
x += 1                 # augmented assignment
C = 300_000_000        # constant by convention; _ is a digit separator
```

**Functions**
```python
def area(width, height=1):          # parameters; height has a default
    """Return the area of a rectangle."""   # docstring: one-line summary
    return width * height

area(3, 4)              # two positional arguments
area(3, height=4)       # one positional, one keyword argument
area(width=3)           # height falls back to its default
```

**The full parameter grammar** — know the names, you won't write all five at once:
```python
def f(a, b, /, c, d=0, *args, e, g=1, **kwargs): ...
#     └ positional-only ┘  └ pos-or-kw ┘ └var-pos┘ └keyword-only┘ └var-kw┘
```

**Returning**
```python
return              # returns None
return value
return a, b         # returns the tuple (a, b); caller does x, y = f()
```

**Conversions**
```python
int("42")        float("3.5")      str(42)       bool("")      # -> False
int(3.9)         # 3, truncates toward zero
int("ff", 16)    # 255, base as second argument
```

**f-strings**
```python
f"{name}"        f"{x:.2f}"       # 2 decimal places
f"{x:>6}"        # right-align in 6 chars      f"{x:,}"    # 1,234,567
f"{r:.1%}"       # 0.25 -> 25.0%               f"{x=}"     # x=5, for debugging
```

**Script entry point**
```python
def main():
    ...

if __name__ == "__main__":
    main()
```

**Catching bad input**
```python
try:
    n = int(input("n: "))
except ValueError:
    print("Not a number")
```

---

## Part 2 — Recall cards

### 1. What is a variable?
A name **bound to an object**. Assignment doesn't copy a value into a box — it points a label at an object in memory. An object is *(docs)* "any data with state (attributes or value) and defined behavior (methods)."

### 2. Is Python typed?
**Dynamically typed and strongly typed.** Dynamic: you never declare a type, and a name can point at a string now and an integer later. Strong: no silent coercion, so `"5" + 5` raises `TypeError`.

### 3. `a = "hi"`, `b = a`, `a = "bye"`. What is `b`?
Still `"hi"`. `b = a` copied the reference; rebinding `a` only moved `a`'s label and didn't touch `b` or the object.

### 4. Statement vs expression?
*(docs)* An expression is "a piece of syntax which can be evaluated to some value." A statement is a construct that does something but needn't produce a value. **Assignment is a statement, not an expression** — which is why `if x = 5` is a syntax error.

### 5. What is a function?
*(docs)* "A series of statements which returns some value to a caller. It can also be passed zero or more arguments which may be used in the execution of the body." Use them for naming a step, reuse, and testability.

### 6. `greet` vs `greet()`?
`greet` is the function object itself — you can pass it around or store it. `greet()` **calls** it. `def` only creates the function object and binds a name to it; the parentheses run the body.

### 7. Parameter vs argument?
*(docs)* A parameter is "a named entity in a function definition that specifies an argument the function can accept." An argument is "a value passed to a function when calling the function." **Definition side vs call side** — and arguments get assigned to the local names in the function body.

### 8. Positional vs keyword argument?
A keyword argument is preceded by an identifier at the call site, like `height=4`; a positional argument isn't. Positional arguments must come first in a call. Keyword arguments are order-independent and self-documenting.

### 9. `return` vs `print`?
`return` hands a value **back to the caller**, so the program can store it, pass it on, or test it. `print` writes text to standard output **for a human** and returns `None`. One is for the program, one is for the person — and a helper that prints instead of returning can't be reused or unit-tested.

### 10. What does a function return with no `return`?
*(docs)* "`return` without an expression argument returns `None`. Falling off the end of a function also returns `None`." Every function returns something.

### 11. How does a function return two values?
It returns one **tuple**: `return a, b` builds `(a, b)`, and the caller unpacks it with `x, y = f()`.

### 12. What is scope?
*(docs)* "The execution of a function introduces a new symbol table used for the local variables." Assignments inside a function go in that local table and die with the call. Lookup goes local → enclosing functions → global → built-ins, which is the **LEGB** rule. Assigning to a global from inside a function needs the `global` keyword; usually that's a sign the value should be a parameter and a return value instead.

### 13. Is Python pass-by-value or pass-by-reference?
*(docs)* "Arguments are passed using call by value, where the value is always an object reference, not the value of the object." So the parameter is a new local name pointing at the same object: **rebinding it is invisible to the caller, mutating the object is not.**

### 14. Mutable vs immutable?
*(docs)* Immutable is "an object with a fixed value… such an object cannot be altered. A new object has to be created if a different value has to be stored" — numbers, strings, tuples. Mutable is "an object with state that is allowed to change" — lists, dicts, sets. So `s.replace("a", "b")` on its own line does nothing; you must assign the result.

### 15. Method vs function?
A method is a function defined inside a class, reached through the dot operator, and it receives the object as its implicit first argument — `self`. `s.lower()` is a method; `len(s)` is a plain function taking the string explicitly.

### 16. Why is `def f(a, L=[])` a bug?
*(docs)* "The default values are evaluated at the point of function definition" and "the default value is evaluated only once" — so every call shares one list and appends pile up across calls. Fix: default to `None` and build a fresh list inside.

### 17. What does `input()` return?
*(docs)* It "reads a line from input, converts it to a string (stripping a trailing newline), and returns that." **Always a string**, even for `42`. Convert with `int()` or `float()` before arithmetic. On EOF it raises `EOFError`.

### 18. `int()` vs `round()`?
`int()` **truncates toward zero**, so `int(-3.7)` is `-3`. `round()` goes to the nearest value, so `round(-3.7)` is `-4`. On a string, `int()` only accepts an integer literal — `int("3.7")` raises `ValueError`.

### 19. The catch in `round()`?
It rounds **half to even**, not half up: `round(0.5)` is `0`, `round(1.5)` is `2`, `round(2.5)` is `2`. And `round(2.675, 2)` gives `2.67`, because most decimals can't be stored exactly as floats.

### 20. `/` vs `//` vs `%`?
`/` is true division and always returns a **float**, so `4 / 2` is `2.0`. `//` floors toward negative infinity, so `-5 // 2` is `-3`. `%` is the remainder. `**` is exponentiation and binds tighter than `*`, so `m * c**2` is `m * (c**2)`.

### 21. Why is `0.1 + 0.2 == 0.3` false?
Floats are binary approximations, so those decimals aren't stored exactly. For money use `decimal.Decimal` or work in integer cents.

### 22. What does `if __name__ == "__main__":` do?
`__name__` is `"__main__"` when the file is **run directly** and the module's own name when it's **imported**. The guard means "only run this as a script", so importing the file to test its functions doesn't execute the program.

### 23. What's falsy in Python?
`None`, `False`, zero of any numeric type, and every empty sequence or mapping — `""`, `[]`, `{}`, `()`. Everything else is truthy, including the string `"0"`.

---

## The spine — if you remember ten lines

1. A variable is a name bound to an object, not a box holding a value.
2. Dynamically typed, strongly typed.
3. `def` creates the function object; `()` runs the body.
4. Parameter is in the definition, argument is at the call.
5. `return` is for the program, `print` is for the human.
6. No `return` means it returns `None`.
7. A function call gets its own local symbol table; lookup is LEGB.
8. Call by value, where the value is an object reference: rebinding is invisible to the caller, mutating isn't.
9. Immutable objects can't be altered, so string methods return a new string you must assign.
10. `input()` always returns a string.
