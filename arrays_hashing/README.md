# Arrays & Hashing

Week 1 of the Blind 75. These problems build the foundation for almost every other pattern —
if you can think in hashmaps reflexively, sliding window, two pointers, and trees become much easier.

---

## Core Idea

A **hashmap** trades space for time. Instead of scanning backwards through an array to find
a value (O(n) per lookup), you store what you've already seen in a dict and look it up in O(1).

The mental model: *"Have I seen the thing I need before?"*

```
for each element:
    if what_i_need is in seen:
        → found the answer
    else:
        → store current element in seen, move on
```

---

## Problems

| # | Problem | Difficulty | Brute Force | Optimal | File |
|---|---------|-----------|-------------|---------|------|
| 1 | Two Sum | Easy | O(n²) / O(1) | O(n) / O(n) | [two_sum.py](two_sum.py) |
| 2 | Valid Anagram | Easy | O(n log n) / O(1) | O(n) / O(n) | [valid_anagram.py](valid_anagram.py) |
| 3 | Contains Duplicate | Easy | O(n²) / O(1) | O(n) / O(n) | [contains_duplicate.py](contains_duplicate.py) |
| 4 | Product of Array Except Self | Medium | O(n²) / O(1) | O(n) / O(1) | [product_except_self.py](product_except_self.py) |
| 5 | Top K Frequent Elements | Medium | O(n log n) / O(n) | O(n) / O(n) | [top_k_frequent.py](top_k_frequent.py) |
| 6 | Encode and Decode Strings | Medium | — | O(n) / O(n) | [encode_decode_strings.py](encode_decode_strings.py) |
| 7 | Group Anagrams | Medium | O(n·k log k) / O(nk) | O(n·k) / O(nk) | [group_anagrams.py](group_anagrams.py) |

---

## Problem Breakdowns

---

### 1. Two Sum

**Problem:** Given `nums` and `target`, return indices of two numbers that sum to target.

**Brute force — O(n²) time, O(1) space**

Check every pair with two nested loops. `j` starts at `i+1` to avoid
pairing an element with itself and to avoid duplicate pairs.

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] + nums[j] == target:
            return [i, j]
```

**Optimal — O(n) time, O(n) space**

For each number, compute its complement (`target - num`).
Check if that complement was already seen. If yes — done.
If no — store the current number and keep going.

Key insight: build the hashmap on the fly, not upfront.
This handles duplicates correctly and exits as early as possible.

```python
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
```

---

### 2. Valid Anagram

**Problem:** Given strings `s` and `t`, return `True` if `t` is an anagram of `s`.

**Brute force — O(n log n) time, O(1) space**

Sort both strings. If they're equal, they're anagrams.
Sorting costs O(n log n) but uses no extra space.

```python
return sorted(s) == sorted(t)
```

**Optimal — O(n) time, O(n) space**

Count character frequencies in both strings using a hashmap.
If the frequency maps are equal, they're anagrams.

```python
if len(s) != len(t):
    return False
count = {}
for c in s:
    count[c] = count.get(c, 0) + 1
for c in t:
    count[c] = count.get(c, 0) - 1
return all(v == 0 for v in count.values())
```

---

### 3. Contains Duplicate

**Problem:** Return `True` if any value appears more than once in `nums`.

**Brute force — O(n²) time, O(1) space**

Compare every pair. If any two are equal, return True.

```python
for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        if nums[i] == nums[j]:
            return True
return False
```

**Optimal — O(n) time, O(n) space**

Use a set. If the current element is already in the set, it's a duplicate.

```python
seen = set()
for num in nums:
    if num in seen:
        return True
    seen.add(num)
return False
```

One-liner alternative: `return len(nums) != len(set(nums))`
(less efficient — builds the full set before checking)

---

### 4. Product of Array Except Self

**Problem:** Return array where `output[i]` is the product of all elements except `nums[i]`.
**Constraint:** Must run in O(n) without using division.

**Brute force — O(n²) time, O(1) space**

For each position, multiply all other elements.

```python
output = []
for i in range(len(nums)):
    product = 1
    for j in range(len(nums)):
        if i != j:
            product *= nums[j]
    output.append(product)
return output
```

**Optimal — O(n) time, O(1) space (excluding output array)**

Two passes: left pass builds prefix products, right pass multiplies in suffix products.

```python
n = len(nums)
output = [1] * n
prefix = 1
for i in range(n):
    output[i] = prefix
    prefix *= nums[i]
suffix = 1
for i in range(n - 1, -1, -1):
    output[i] *= suffix
    suffix *= nums[i]
return output
```

Key insight: `output[i]` = (product of everything left of i) × (product of everything right of i).
Prefix pass handles the left side, suffix pass handles the right side.

---

### 5. Top K Frequent Elements

**Problem:** Return the `k` most frequent elements in `nums`.

**Brute force — O(n log n) time, O(n) space**

Count frequencies, sort by frequency descending, return top k.

```python
count = {}
for num in nums:
    count[num] = count.get(num, 0) + 1
sorted_items = sorted(count, key=lambda x: count[x], reverse=True)
return sorted_items[:k]
```

**Optimal — O(n) time, O(n) space (bucket sort)**

Since frequencies range from 1 to n, use an array of buckets indexed by frequency.
Then scan from highest frequency bucket down to collect k elements.

```python
count = {}
for num in nums:
    count[num] = count.get(num, 0) + 1
buckets = [[] for _ in range(len(nums) + 1)]
for num, freq in count.items():
    buckets[freq].append(num)
result = []
for freq in range(len(buckets) - 1, 0, -1):
    for num in buckets[freq]:
        result.append(num)
        if len(result) == k:
            return result
```

---

### 6. Encode and Decode Strings

**Problem:** Design encode/decode functions to serialize a list of strings to a single string
and deserialize it back. Must handle any character including `/` and empty strings.

**Key insight:** You can't use a simple delimiter like `,` because strings may contain it.
Use a **length-prefixed encoding**: `"<length>#<string>"` for each word.

```python
# Encode: prepend each string with its length + '#'
# "hello", "world" → "5#hello5#world"

def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    result, i = [], 0
    while i < len(s):
        j = s.index("#", i)          # find the next '#'
        length = int(s[i:j])         # read the length
        result.append(s[j+1:j+1+length])  # extract the string
        i = j + 1 + length           # advance past it
    return result
```

Time: O(n) encode, O(n) decode — n = total characters across all strings
Space: O(n) for the encoded string

---

### 7. Group Anagrams

**Problem:** Given a list of strings, group anagrams together.

**Approach — O(n·k log k) time, O(nk) space**

Sort each string to get a canonical key. Strings that are anagrams
produce the same sorted key. Group them in a hashmap.

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))   # "eat" → "aet", "tea" → "aet"
        groups[key].append(s)
    return list(groups.values())
```

**Optimal — O(n·k) time using character count as key**

Instead of sorting (O(k log k)), count character frequencies (O(k)).
Use a tuple of 26 counts as the hashmap key.

```python
def group_anagrams_optimal(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())
```

---

## Complexity Summary

| Problem | Brute Time | Brute Space | Optimal Time | Optimal Space |
|---------|-----------|-------------|-------------|---------------|
| Two Sum | O(n²) | O(1) | O(n) | O(n) |
| Valid Anagram | O(n log n) | O(1) | O(n) | O(n) |
| Contains Duplicate | O(n²) | O(1) | O(n) | O(n) |
| Product Except Self | O(n²) | O(1) | O(n) | O(1) |
| Top K Frequent | O(n log n) | O(n) | O(n) | O(n) |
| Encode & Decode | — | — | O(n) | O(n) |
| Group Anagrams | O(n·k log k) | O(nk) | O(n·k) | O(nk) |

---

## Running the tests

Each file has inline tests runnable directly:

```bash
python two_sum.py
python valid_anagram.py
# etc.
```

Or run all at once from the repo root:

```bash
for f in arrays_hashing/*.py; do python "$f"; done
```
