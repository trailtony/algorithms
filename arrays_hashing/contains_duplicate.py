# ─────────────────────────────────────────────────────────────
# CONTAINS DUPLICATE
# https://leetcode.com/problems/contains-duplicate/
# Difficulty: Easy
# ─────────────────────────────────────────────────────────────
#
# PROBLEM
# Given an integer array nums, return True if any value appears
# at least twice, and False if every element is distinct.
#
# Example:
#   nums = [1, 2, 3, 1]  → True  (1 appears twice)
#   nums = [1, 2, 3, 4]  → False (all distinct)
#   nums = [1, 1, 1, 3]  → True  (1 appears three times)
#
# ┌──────────────────────────────┬────────────┬────────────┐
# │ Approach                     │ Time       │ Space      │
# ├──────────────────────────────┼────────────┼────────────┤
# │ Brute force (nested loops)   │ O(n²)      │ O(1)       │
# │ Set length comparison        │ O(n)       │ O(n)       │
# │ Early-exit hashset (optimal) │ O(n)       │ O(n)       │
# └──────────────────────────────┴────────────┴────────────┘
# ─────────────────────────────────────────────────────────────

from typing import List


# ── APPROACH 1: Brute Force (Nested Loops) ───────────────────
# Compare every pair of elements. If any two are equal, return True.
# j always starts at i+1 to avoid comparing an element with itself
# and to avoid checking the same pair twice.
#
# This is the most intuitive approach — no extra data structures,
# just raw comparison. The trade-off is the quadratic time cost.
#
# Time:  O(n²) — for n elements there are n*(n-1)/2 pairs to check
# Space: O(1)  — only two index variables, no extra data structure

def contains_duplicate_brute(nums: List[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


# ── APPROACH 2: Set Length Comparison ────────────────────────
# A set only stores unique values. If converting nums to a set
# produces fewer elements, at least one duplicate was removed.
#
# Concise and readable — your submitted solution (cleaned up).
# The if nums guard is not needed: an empty list gives
# len([]) > len(set([])) → 0 > 0 → False, which is correct.
#
# One limitation: set(nums) always completes a full pass through
# the entire array before any comparison happens. There is no
# early exit — even if the first two elements are duplicates,
# Python still builds the entire set first.
#
# Time:  O(n) — building the set requires one full pass
# Space: O(n) — the set holds up to n unique elements

def contains_duplicate_set(nums: List[int]) -> bool:
    return len(nums) > len(set(nums))


# ── APPROACH 3: Early-Exit Hashset (Optimal) ─────────────────
# Build the seen set one element at a time. The moment a number
# is already in seen we have found a duplicate — return True
# immediately without processing the rest of the array.
#
# Best case: O(1) if the first two elements are duplicates.
# Worst case: O(n) if there are no duplicates (full pass).
#
# This is strictly better than the set comparison approach
# because it can exit early. Same asymptotic complexity but
# faster in practice whenever duplicates appear early in the array.
#
# Time:  O(n) — at most one full pass, exits as soon as duplicate found
# Space: O(n) — seen set holds up to n elements in the worst case

def contains_duplicate(nums: List[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


# ─────────────────────────────────────────────────────────────
# Tests — run with: python contains_duplicate.py
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Duplicate exists
    assert contains_duplicate_brute([1, 2, 3, 1])    == True
    assert contains_duplicate_brute([1, 1, 1, 3])    == True
    # All distinct
    assert contains_duplicate_brute([1, 2, 3, 4])    == False
    # Duplicate at the very start — early-exit advantage
    assert contains_duplicate_brute([1, 1, 5, 6])    == True
    # Single element — can't be a duplicate
    assert contains_duplicate_brute([1])              == False
    # Empty array — no duplicates
    assert contains_duplicate_brute([])               == False
    # Negative numbers
    assert contains_duplicate_brute([-1, -2, -3, -1]) == True

    assert contains_duplicate_set([1, 2, 3, 1])      == True
    assert contains_duplicate_set([1, 1, 1, 3])      == True
    assert contains_duplicate_set([1, 2, 3, 4])      == False
    assert contains_duplicate_set([1, 1, 5, 6])      == True
    assert contains_duplicate_set([1])               == False
    assert contains_duplicate_set([])                == False
    assert contains_duplicate_set([-1, -2, -3, -1])  == True

    assert contains_duplicate([1, 2, 3, 1])          == True
    assert contains_duplicate([1, 1, 1, 3])          == True
    assert contains_duplicate([1, 2, 3, 4])          == False
    assert contains_duplicate([1, 1, 5, 6])          == True
    assert contains_duplicate([1])                   == False
    assert contains_duplicate([])                    == False
    assert contains_duplicate([-1, -2, -3, -1])      == True

    print("All tests passed.")