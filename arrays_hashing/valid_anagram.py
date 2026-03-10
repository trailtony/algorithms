# ─────────────────────────────────────────────────────────────
# VALID ANAGRAM
# https://leetcode.com/problems/valid-anagram/
# Difficulty: Easy
# ─────────────────────────────────────────────────────────────
#
# PROBLEM
# Given two strings s and t, return True if t is an anagram of s,
# and False otherwise.
# An anagram is a word formed by rearranging the letters of another
# using all the original letters exactly once.
#
# Example:
#   s = "anagram", t = "nagaram" → True
#   s = "rat",     t = "car"     → False
#
# ┌─────────────────────────────┬──────────────┬──────────────┐
# │ Approach                    │ Time         │ Space        │
# ├─────────────────────────────┼──────────────┼──────────────┤
# │ Brute force (sorting)       │ O(n log n)   │ O(n)         │
# │ Optimal (frequency hashmap) │ O(n)         │ O(n)         │
# └─────────────────────────────┴──────────────┴──────────────┘
# ─────────────────────────────────────────────────────────────


# ── APPROACH 1: Brute Force (Sorting) ────────────────────────
# If two strings are anagrams, sorting both produces the same result.
# "anagram" sorted → "aaagmnr"
# "nagaram" sorted → "aaagmnr"  ← identical, so they're anagrams
#
# Simple and correct, but sorting costs O(n log n) and Python's
# sorted() creates a new list for each string, so space is O(n).
#
# Time:  O(n log n) — dominated by the sort step
# Space: O(n)       — sorted() returns a new list of n characters

def is_anagram_brute(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)


# ── APPROACH 2: Optimal (Frequency Hashmap) ──────────────────
# Count character frequencies for both strings using a hashmap.
# If every character appears the same number of times in both,
# they are anagrams.
#
# Early exit: if lengths differ they can't be anagrams —
# skips both loops entirely and avoids building any maps.
#
# Two separate maps makes the logic easy to reason about:
# build s_map for s, build t_map for t, compare them.
# Python's dict equality checks both keys and values, so
# s_map == t_map is a clean one-line comparison.
#
# Note: for lowercase English letters only, maps hold at most
# 26 keys, so space is effectively O(1) in that constraint —
# but we say O(n) to be general (Unicode strings could have
# as many unique characters as the string is long).
#
# Time:  O(n) — two passes (one over s, one over t) + one comparison
# Space: O(n) — two frequency maps, at most n unique keys each

def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    s_map = {}
    t_map = {}

    for c in s:
        s_map[c] = s_map.get(c, 0) + 1

    for c in t:
        t_map[c] = t_map.get(c, 0) + 1

    return s_map == t_map


# ── ALTERNATIVE OPTIMAL: Single Balance Map ───────────────────
# Instead of two maps, use one map as a balance counter.
# Increment for each character in s, decrement for each in t.
# If all values are zero at the end, every character that
# appeared in s was cancelled out by t → anagram.
#
# Advantage: half the memory of the two-map approach.
# Trade-off: slightly less readable at a glance.
#
# Time:  O(n) — two passes + one scan over at most n keys
# Space: O(n) — one frequency map

def is_anagram_single_map(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    count = {}

    for c in s:
        count[c] = count.get(c, 0) + 1

    for c in t:
        count[c] = count.get(c, 0) - 1

    return all(v == 0 for v in count.values())


# ─────────────────────────────────────────────────────────────
# Tests — run with: python valid_anagram.py
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Standard anagram
    assert is_anagram_brute("anagram", "nagaram") == True
    assert is_anagram_brute("rat", "car")         == FalseW
    # Different lengths — must be False
    assert is_anagram_brute("ab", "abc")          == False
    # Same characters different counts
    assert is_anagram_brute("aab", "bba")         == False
    # Single characters
    assert is_anagram_brute("a", "a")             == True
    assert is_anagram_brute("a", "b")             == False
    # Empty strings — two empty strings are anagrams of each other
    assert is_anagram_brute("", "")               == True

    assert is_anagram("anagram", "nagaram")       == True
    assert is_anagram("rat", "car")               == False
    assert is_anagram("ab", "abc")                == False
    assert is_anagram("aab", "bba")               == False
    assert is_anagram("a", "a")                   == True
    assert is_anagram("a", "b")                   == False
    assert is_anagram("", "")                     == True

    assert is_anagram_single_map("anagram", "nagaram") == True
    assert is_anagram_single_map("rat", "car")         == False
    assert is_anagram_single_map("ab", "abc")          == False
    assert is_anagram_single_map("aab", "bba")         == False
    assert is_anagram_single_map("a", "a")             == True
    assert is_anagram_single_map("a", "b")             == False
    assert is_anagram_single_map("", "")               == True

    print("All tests passed.")