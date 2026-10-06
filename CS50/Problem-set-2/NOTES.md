# Loops, Lists, Tuples, Dicts & Sets — Interview Recall Sheet

Part 1 is syntax you should be able to write cold. Part 2 is questions with the answer phrased the way you'd **say it out loud** — read the question, answer from memory, check. Definitions marked *(docs)* are quoted from docs.python.org, so you can say them verbatim.

---

## Part 1 — Syntax

### Loops

**`for`** — iterate over the items, not the indices:
```python
for char in word:              # strings are iterable
    print(char)

for i in range(5):             # 0 1 2 3 4
for i in range(2, 10, 3):      # 2 5 8   (start, stop, step)
for i in range(len(s) - 1, -1, -1):   # backwards; or just reversed(s)
```

**`while`** — when you don't know the count up front:
```python
while inserted < 50:           # condition tested BEFORE each pass
    inserted += int(input("Insert Coin: "))

while True:                    # loop forever, exit explicitly
    line = input("> ")
    if not line:
        break
```

**Loop control**
```python
break        # leave the loop now; skips the else clause
continue     # skip to the next iteration
pass         # do nothing (a syntactic placeholder, not loop control)
else:        # runs only if the loop finished WITHOUT break
```

**The iteration helpers you should reach for**
```python
for i, char in enumerate(word):          # index and item
for i, char in enumerate(word, 1):       # start counting at 1
for name, cal in zip(fruits, calories):  # walk two sequences together
for x in reversed(items):
for x in sorted(items, key=str.lower, reverse=True):
```

**Comprehensions** — a loop that evaluates to a collection:
```python
[c for c in s if c not in "aeiou"]           # list
{c for c in s}                               # set
{k: v for k, v in zip(keys, vals)}           # dict
sum(1 for c in s if c.isdigit())             # generator, no list built
```

**Aggregating in one call**
```python
sum(xs)   max(xs)   min(xs)   len(xs)
any(c.isdigit() for c in s)      # True if at least one
all(c.isalnum() for c in s)      # True if every one (True for empty!)
```

### Lists — ordered, mutable, indexable
```python
xs = [1, 2, 3]        xs = list("abc")       xs = []
xs[0]     xs[-1]      # first, last
xs[1:3]   xs[::-1]    xs[:]      # slice; reversed copy; shallow copy
xs.append(4)          xs.extend([5, 6])      xs.insert(0, 9)
xs.pop()   xs.pop(0)  xs.remove(2)           del xs[0]
xs.sort()             xs.sort(key=len)       # IN PLACE, returns None
sorted(xs)                                   # returns a NEW list
xs.index(2)   xs.count(2)   2 in xs
rows = [[0] * 3 for _ in range(2)]           # a 2D grid, done right
```

### Tuples — ordered, **immutable**, hashable
```python
t = (1, 2)      t = 1, 2         # parentheses are optional
t = (1,)                         # ONE-element tuple needs the comma
t = ()
x, y = t                         # unpacking
for a, b in pairs: ...           # unpacking in a for
t.index(2)   t.count(2)   2 in t # no append, no sort, no item assignment
```

### Dicts — key → value, mutable, insertion-ordered
```python
d = {"apple": 130, "lemon": 15}       d = dict(apple=130)       d = {}
d["apple"]          # KeyError if missing
d.get("kiwi")       # None if missing
d.get("kiwi", 0)    # default if missing
d["kiwi"] = 90      # insert or overwrite
d.setdefault("k", []).append(1)       # get-or-create, then mutate
del d["apple"]      d.pop("apple")    d.pop("apple", None)
"apple" in d        # tests KEYS
for k in d:                  ...      # keys
for v in d.values():         ...
for k, v in d.items():       ...
len(d)   d.update(other)     d.clear()
```

### Sets — unordered, no duplicates, members must be hashable
```python
s = {1, 2, 3}       s = set("hello")    s = set()     # {} is an empty DICT
s.add(4)    s.discard(4)   s.remove(4)  # remove raises KeyError, discard doesn't
3 in s                                  # O(1)
a | b    a & b    a - b    a ^ b        # union, intersection, difference, symmetric
len(set(xs))                            # count of distinct items
```

### String methods that drive loops
```python
"".join(chars)       "-".join(parts)    # build a string from pieces
s.split()            s.split(":")
c.isupper()  c.islower()  c.isalpha()  c.isdigit()  c.isalnum()
c.lower()    c.upper()
```

---

## Part 2 — Recall cards

### 1. `for` vs `while` — how do you choose?
`for` iterates over a **known sequence of items** — the characters of a string, the rows of a list, `range(n)`. `while` repeats on a **condition** when you can't say up front how many passes there'll be: reading input until the total reaches 50, retrying until valid. If you find yourself maintaining a counter by hand in a `while`, it wanted to be a `for`.

### 2. What is an iterable? An iterator?
*(docs)* An iterable is "an object capable of returning its members one at a time." An iterator *(docs)* "represents a stream of data" and is what `for` actually drives: `for` calls `iter()` on your iterable to get an iterator, then `next()` until `StopIteration`. Lists, tuples, strings, dicts, sets, files and ranges are all iterable; an iterator is **consumed once** and is empty afterwards.

### 3. What does `range` return?
A lazy `range` object, not a list — it computes values on demand, so `range(10**9)` costs nothing. Call `list(range(...))` if you really need the list. `range(start, stop, step)` is **half-open**: `stop` is excluded, which is why `range(len(xs))` covers every valid index exactly once.

### 4. `for char in s:` vs `for i in range(len(s)):`?
Iterate the items directly unless you genuinely need the index — it's shorter, can't go out of range, and works on anything iterable. When you need both, that's `enumerate(s)`, not manual indexing.

### 5. What does `enumerate` give you?
An iterator of `(index, item)` tuples, which the `for` unpacks: `for i, char in enumerate(s):`. A second argument changes the starting number — `enumerate(s, 1)` — without affecting the items.

### 6. What does `zip` do, and where's the trap?
It walks several iterables in parallel, yielding tuples of their i-th items. The trap: it **stops at the shortest** and silently drops the rest, so a mismatched pair of lists loses data with no error. `zip(a, b, strict=True)` raises instead (3.10+), and `itertools.zip_longest` pads.

### 7. Two parallel lists vs one dict?
A dict. Two lists zipped together are a dict with the invariants unenforced — nothing keeps them the same length or in the same order, and lookup is a **O(n) scan** rather than an O(1) hash. `{"apple": 130}.get(fruit, "")` replaces the whole search loop with one expression.

### 8. `break` vs `continue` vs `return` in a loop?
`break` exits the loop and continues after it. `continue` abandons this iteration and starts the next one. `return` exits the whole **function**, loop included — which is often the cleanest way out of a search loop, since you return the moment you find the answer.

### 9. What is `for ... else`?
The `else` block runs when the loop **completed without hitting `break`** — i.e. "we searched everything and found nothing." It does *not* mean "if the loop body never ran." Useful for the not-found case, though returning from inside the loop usually reads better.

### 10. Why is mutating a list while iterating it a bug?
The iterator tracks a position by index, so removing an item shifts everything left and the loop **skips the next element**. `for x in [1,2,3,4]: if x % 2 == 0: l.remove(x)` leaves `[1, 3]` — the `4` is never examined. Iterate over a copy (`for x in l[:]`) or build a new list with a comprehension.

### 11. `+=` on a string in a loop — what's really happening?
Strings are immutable, so each `+=` builds a **brand-new string** and copies everything so far: n characters means O(n²) copying. Fine for a 20-character licence plate, wrong for a large file. The idiom is to collect pieces in a list and `"".join(pieces)` once, which is O(n).

### 12. List vs tuple — when does it matter?
Both are ordered sequences; a list is **mutable** and a tuple is **immutable**. So a tuple can be a dict key or a set member (it's hashable, assuming its contents are), it signals "this won't change", and it unpacks cleanly — `hours, minutes = s.split(":")`. A list is for a homogeneous collection you'll grow, sort, or edit. `hash([1,2])` raises `TypeError: unhashable type: 'list'`.

### 13. How do you write a one-element tuple?
`(1,)` — **the comma makes the tuple**, not the parentheses. `(1)` is just the integer `1` in parentheses. `1, 2` without parentheses is already a tuple, which is how `return a, b` returns two values.

### 14. What makes a valid dict key or set member?
It must be **hashable**: *(docs)* an object with a hash value "which never changes during its lifetime". That means immutable in practice — strings, numbers, tuples of those. Lists, dicts and sets are unhashable, so they can't be keys. Hashing is what buys O(1) lookup.

### 15. Are dicts ordered?
Yes — since Python 3.7 a dict **preserves insertion order**, and that's a language guarantee, not an implementation detail. It is *not* sorted order: `sorted(d)` gives the keys sorted. Sets have **no order at all**, and the order you see when printing one is not something to rely on.

### 16. `d["k"]` vs `d.get("k")`?
`d["k"]` raises `KeyError` when the key is missing; `d.get("k")` returns `None`, and `d.get("k", default)` returns your own fallback. Use the brackets when a missing key is a bug you want to hear about, and `.get` when absence is an expected, handleable case.

### 17. What does `setdefault` do?
It returns the value for a key, inserting a default first if the key isn't there — so `d.setdefault(k, []).append(x)` is the one-liner for building a dict of lists. (`collections.defaultdict(list)` does the same thing for a whole dict.)

### 18. How do you iterate a dict's keys and values together?
`for k, v in d.items():` — `items()` yields `(key, value)` tuples which the `for` unpacks. Iterating the dict itself (`for k in d:`) gives **keys only**, and `d.values()` gives values only. All three are lazy **views** over the live dict, so mutating the dict mid-loop raises `RuntimeError: dictionary changed size during iteration`.

### 19. When do you want a set?
For membership tests, and for deduplicating. `x in some_set` is O(1) hashed, versus O(n) scanning a list, so a set is the right type for "is this a vowel", "have I seen this already", "which words are in both lists". It also gives you real set algebra: `a & b`, `a | b`, `a - b`.

### 20. How do you make an empty set?
`set()`. `{}` is an **empty dict** — the braces belong to dicts first, and a set literal needs at least one element, like `{1}`.

### 21. What is a list comprehension and when shouldn't you use one?
`[expr for item in iterable if cond]` — one expression that builds a list, replacing the three-line append loop, and it's usually faster because the append is done in C. Skip it when the body needs several statements, when you're nesting more than two `for`s, or when the point is a **side effect** rather than a new collection; a loop you wrote for its side effects should look like a loop.

### 22. Comprehension in `[]` vs `()`?
`[...]` builds the whole list in memory. `(...)` is a **generator expression** that produces items one at a time, so `sum(1 for c in s if c.isdigit())` counts without ever materialising a list — the right choice for large data and for feeding `sum`, `any`, `all`, `max`.

### 23. `any` vs `all` on an empty iterable?
`any([])` is `False` and `all([])` is **`True`** — vacuous truth, "no counterexample exists." That bites in validation: `all(c.isalnum() for c in s)` happily passes the empty string, so check the length separately.

### 24. `xs.sort()` vs `sorted(xs)`?
`xs.sort()` sorts **in place and returns `None`**, so `xs = xs.sort()` destroys your list — a classic. `sorted(xs)` leaves the original alone and returns a new list, and it accepts any iterable. Same for `xs.reverse()` versus `reversed(xs)`. Both take `key=` (a function applied to each item before comparing) and `reverse=True`.

### 25. `ys = xs` then `ys.append(4)` — what is `xs`?
`[1, 2, 3, 4]`. `ys = xs` binds a second name to the **same list object**, so both see the mutation. `ys = xs[:]` (or `list(xs)`, or `copy.copy`) makes a shallow copy — but the copy's *elements* are still shared, which is why `copy.deepcopy` exists for nested structures.

### 26. Why is `[[0] * 3] * 2` broken?
`*` on a list repeats **references**, so you get two names for one inner list and `grid[0][0] = 9` appears to change both rows. Build it with a comprehension — `[[0] * 3 for _ in range(2)]` — which evaluates a fresh inner list per row.

### 27. How do you count or group things?
A dict keyed by the thing: `counts[c] = counts.get(c, 0) + 1`. `collections.Counter(s)` does exactly this in one call and gives you `.most_common()`, and `collections.defaultdict(list)` groups into lists.

### 28. How do you know a `while` loop will end?
Something inside it must move the condition toward `False` on every pass. If the state only changes inside an `if` — the coke machine that only credits valid coins — then an invalid input makes the pass a no-op, and the loop is correct only because the user can keep trying. Check that there's no path through the body that changes nothing *and* can repeat forever.

### 29. `is` vs `==` on containers?
`==` compares contents element by element, so `[1, 2] == [1, 2]` is `True`. `is` compares identity, so the same expression with `is` is `False`. Also note `[] == ()` is `False` — different types never compare equal as sequences — while `{1, 2} == {2, 1}` is `True`, because a set has no order.

### 30. What does unpacking do in a `for`?
Each item is assigned to several names at once, so `for name, cal in zip(a, b):` binds both per iteration. It needs the item to be a sequence of exactly that length, otherwise `ValueError`. `*rest` absorbs the remainder: `first, *rest = xs`.

---

## The spine — if you remember ten lines

1. `for` iterates a known sequence; `while` repeats on a condition.
2. Iterate items, not indices — and `enumerate` when you need both.
3. `zip` stops at the shortest input, silently.
4. Two parallel lists want to be one dict: O(1) lookup, invariants enforced.
5. Never mutate a list while iterating it — you'll skip elements.
6. `+=` on a string in a loop is O(n²); collect in a list and `"".join`.
7. Tuples are immutable and hashable, so they can be dict keys; lists can't.
8. Dicts keep insertion order; sets have no order.
9. `xs.sort()` returns `None` and mutates; `sorted(xs)` returns a new list.
10. `ys = xs` shares one object; `xs[:]` copies the list but not its elements.
