# ─────────────────────────────────────────────────────────────
# TWO SUM
# https://leetcode.com/problems/two-sum/
# Difficulty: Easy
# ─────────────────────────────────────────────────────────────
#
# PROBLEM
# Given an array of integers `nums` and an integer `target`,
# return the indices of the two numbers that add up to target.
# Exactly one solution exists. You may not use the same element twice.
#
# ┌─────────────────────┬──────────────┬──────────────┐
# │ Approach            │ Time         │ Space        │
# ├─────────────────────┼──────────────┼──────────────┤
# │ Brute force         │ O(n²)        │ O(1)         │
# │ Hashmap (optimal)   │ O(n)         │ O(n)         │
# └─────────────────────┴──────────────┴──────────────┘
# ─────────────────────────────────────────────────────────────

from typing import List


# ── APPROACH 1: Brute Force ───────────────────────────────────
# Check every possible pair using two nested loops.
# Outer loop picks the first number, inner loop picks the second.
# j always starts at i+1 to avoid pairing an element with itself
# and to avoid checking the same pair twice.
#
# Time:  O(n²) — for n elements there are n*(n-1)/2 pairs to check
# Space: O(1)  — no extra data structure, just two index variables

def two_sum_brute(nums: List[int], target: int) -> List[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]


# ── APPROACH 2: Hashmap (Optimal) ────────────────────────────
# For each number, compute its complement (target - num).
# If that complement is already in the hashmap we found our pair.
# Otherwise store the current number and its index for future lookups.
#
# Building seen on the fly (not pre-loading) means:
#   - We exit as early as possible (first valid pair found)
#   - Duplicate values are handled correctly because we check
#     the complement BEFORE inserting the current number
#
# Time:  O(n)  — single pass, each lookup and insert is O(1)
# Space: O(n)  — seen dict holds up to n entries in the worst case
#                (worst case: answer is the very last pair)

def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}  # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i


# ─────────────────────────────────────────────────────────────
# Tests — run with: python two_sum.py
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Basic case
    assert two_sum_brute([2, 7, 11, 15], 9)  == [0, 1]
    assert two_sum_brute([3, 2, 4], 6)        == [1, 2]
    # Duplicate values — must not pair element with itself
    assert two_sum_brute([3, 3], 6)           == [0, 1]
    # Answer at the end of the array
    assert two_sum_brute([1, 2, 3, 4], 7)     == [2, 3]

    assert two_sum([2, 7, 11, 15], 9)         == [0, 1]
    assert two_sum([3, 2, 4], 6)              == [1, 2]
    assert two_sum([3, 3], 6)                 == [0, 1]
    assert two_sum([1, 2, 3, 4], 7)           == [2, 3]

    print("All tests passed.")