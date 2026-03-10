# Algorithms — Blind 75 Study Repo

30-day algorithm practice repo following the Blind 75 list.
Each folder maps to one week of the plan. Every problem has
both a brute force and optimal solution with full complexity analysis.

---

## Structure

```
algorithms/
├── arrays_hashing/      Week 1 — foundation patterns
├── sliding_window/      Week 2
├── two_pointers/        Week 2
├── stack/               Week 3
├── binary_search/       Week 3
└── trees/               Week 4
```

---

## Problem Index

### Week 1 — Arrays & Hashing

| Problem | Optimal Time | Optimal Space | Link |
|---------|-------------|---------------|------|
| Two Sum | O(n) | O(n) | [arrays_hashing/two_sum.py](arrays_hashing/two_sum.py) |
| Valid Anagram | O(n) | O(n) | [arrays_hashing/valid_anagram.py](arrays_hashing/valid_anagram.py) |
| Contains Duplicate | O(n) | O(n) | [arrays_hashing/contains_duplicate.py](arrays_hashing/contains_duplicate.py) |
| Product of Array Except Self | O(n) | O(1) | [arrays_hashing/product_except_self.py](arrays_hashing/product_except_self.py) |
| Top K Frequent Elements | O(n) | O(n) | [arrays_hashing/top_k_frequent.py](arrays_hashing/top_k_frequent.py) |
| Encode and Decode Strings | O(n) | O(n) | [arrays_hashing/encode_decode_strings.py](arrays_hashing/encode_decode_strings.py) |
| Group Anagrams | O(n·k) | O(nk) | [arrays_hashing/group_anagrams.py](arrays_hashing/group_anagrams.py) |

### Week 2 — Sliding Window & Two Pointers

| Problem | Optimal Time | Optimal Space | Link |
|---------|-------------|---------------|------|
| Minimum Window Substring | O(n) | O(n) | [sliding_window/minimum_window_substring.py](sliding_window/minimum_window_substring.py) |
| Longest Substring Without Repeating Chars | O(n) | O(n) | [sliding_window/longest_substring.py](sliding_window/longest_substring.py) |
| Longest Repeating Character Replacement | O(n) | O(1) | [sliding_window/longest_repeating_replacement.py](sliding_window/longest_repeating_replacement.py) |
| Permutation in String | O(n) | O(1) | [sliding_window/permutation_in_string.py](sliding_window/permutation_in_string.py) |
| Container With Most Water | O(n) | O(1) | [two_pointers/container_with_most_water.py](two_pointers/container_with_most_water.py) |
| Two Sum II | O(n) | O(1) | [two_pointers/two_sum_ii.py](two_pointers/two_sum_ii.py) |
| 3Sum | O(n²) | O(1) | [two_pointers/three_sum.py](two_pointers/three_sum.py) |

### Week 3 — Stack & Binary Search

| Problem | Optimal Time | Optimal Space | Link |
|---------|-------------|---------------|------|
| Valid Parentheses | O(n) | O(n) | [stack/valid_parentheses.py](stack/valid_parentheses.py) |
| Min Stack | O(1) | O(n) | [stack/min_stack.py](stack/min_stack.py) |
| Evaluate Reverse Polish Notation | O(n) | O(n) | [stack/evaluate_rpn.py](stack/evaluate_rpn.py) |
| Generate Parentheses | O(4ⁿ/√n) | O(n) | [stack/generate_parentheses.py](stack/generate_parentheses.py) |
| Binary Search | O(log n) | O(1) | [binary_search/binary_search.py](binary_search/binary_search.py) |
| Search in Rotated Sorted Array | O(log n) | O(1) | [binary_search/search_rotated.py](binary_search/search_rotated.py) |
| Find Minimum in Rotated Sorted Array | O(log n) | O(1) | [binary_search/find_minimum_rotated.py](binary_search/find_minimum_rotated.py) |

### Week 4 — Trees

| Problem | Optimal Time | Optimal Space | Link |
|---------|-------------|---------------|------|
| Invert Binary Tree | O(n) | O(h) | [trees/invert_binary_tree.py](trees/invert_binary_tree.py) |
| Maximum Depth of Binary Tree | O(n) | O(h) | [trees/max_depth.py](trees/max_depth.py) |
| Same Tree | O(n) | O(h) | [trees/same_tree.py](trees/same_tree.py) |
| Subtree of Another Tree | O(n·m) | O(h) | [trees/subtree.py](trees/subtree.py) |
| Lowest Common Ancestor of BST | O(h) | O(1) | [trees/lowest_common_ancestor.py](trees/lowest_common_ancestor.py) |
| Binary Tree Level Order Traversal | O(n) | O(n) | [trees/level_order_traversal.py](trees/level_order_traversal.py) |
| Validate Binary Search Tree | O(n) | O(h) | [trees/validate_bst.py](trees/validate_bst.py) |

*h = tree height. O(h) = O(log n) for balanced trees, O(n) worst case.*

---

## File Template

Every problem follows the same structure:

```
# ─────────────────────────────────────────────
# PROBLEM NAME
# LeetCode link
# Difficulty
# ─────────────────────────────────────────────
# PROBLEM statement
#
# ┌─────────────────┬──────────┬──────────┐
# │ Approach        │ Time     │ Space    │
# ├─────────────────┼──────────┼──────────┤
# │ Brute force     │ O(?)     │ O(?)     │
# │ Optimal         │ O(?)     │ O(?)     │
# └─────────────────┴──────────┴──────────┘

# APPROACH 1: Brute Force
# explanation
def solution_brute(...): ...

# APPROACH 2: Optimal
# explanation
def solution(...): ...

# Tests
if __name__ == "__main__":
    assert solution_brute(...) == ...
    assert solution(...) == ...
    print("All tests passed.")
```

---

## Running tests

Single file:
```bash
python arrays_hashing/two_sum.py
```

All files in a folder:
```bash
for f in arrays_hashing/*.py; do python "$f"; done
```

All files in the repo:
```bash
find . -name "*.py" | xargs -I {} python {}
```
