from collections import defaultdict
from typing import List
import unittest
# Why these imports:
# - defaultdict(list): creates an empty list for a new key automatically,
#   so grouping logic can append directly without manual key checks.
# - List: adds clear type hints for inputs/outputs, improving readability
#   and helping static analyzers/editors catch type issues early.


# ─────────────────────────────────────────────────────────────
# GROUP ANAGRAMS
# https://leetcode.com/problems/group-anagrams/
# Difficulty: Medium
# ─────────────────────────────────────────────────────────────
#
# PROBLEM
# Given an array of strings strs, group the anagrams together.
# You can return the answer in any order.
#
# Example:
#   strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
#   output can be: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
#
# ┌──────────────────────────────┬────────────────┬──────────────┐
# │ Approach                     │ Time           │ Space        │
# ├──────────────────────────────┼────────────────┼──────────────┤
# │ Sorted-key hashmap           │ O(n * k log k) │ O(n * k)     │
# │ Character-count hashmap      │ O(n * k)       │ O(n * k)     │
# └──────────────────────────────┴────────────────┴──────────────┘
# ─────────────────────────────────────────────────────────────
#
# n = number of strings
# k = maximum string length



class Solution:
    # LeetCode expected method name (uses optimal approach)
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        return self.groupAnagramsCount(strs)

    # ── APPROACH 1: Sorted-Key Hashmap ───────────────────────────
    # Interview framing:
    # - Build a canonical signature per word so anagrams collapse to one key.
    # - Sorting gives that canonical form regardless of original character order.
    # - Store by key in hashmap: key -> list of matching words.
    #
    # Why interviewer may like this:
    # - Very readable and easy to explain correctly.
    # - Works naturally even when character set is not limited to a-z.
    #
    # Tradeoff:
    # - Sorting each word is the expensive step.
    # - Prefer this when code clarity/general character support matters most.
    #
    # Sort each word and use the sorted string as a canonical key.
    # Anagrams produce the same sorted key, so they land in the same bucket.
    #
    # Example:
    #   "eat" -> "aet"
    #   "tea" -> "aet"
    #   "ate" -> "aet"   (all grouped together)
    #
    # Time complexity (detailed):
    # - We process n words.
    # - Sorting one word of length k costs O(k log k).
    # - Hash insertion/appending per word is O(1) average.
    # - Total: O(n * k log k).
    #
    # Space complexity (detailed):
    # - Hashmap stores all input words across groups -> O(n * k) total character storage.
    # - Sorted keys also require extra storage; in the worst case, total key size is O(n * k).
    # - Ignoring output would still require O(n * k) auxiliary storage for grouping.
    # - Total: O(n * k).
    def groupAnagramsSorted(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)

        for word in strs:
            key = "".join(sorted(word))
            groups[key].append(word)

        return list(groups.values())

    # ── APPROACH 2: Character-Count Hashmap (Optimal) ───────────
    # Interview framing:
    # - Keep the same "canonical signature" idea, but avoid sorting.
    # - Use a 26-slot frequency vector as the key for each word.
    # - Words with identical counts are anagrams and map to the same bucket.
    #
    # Why interviewer may like this:
    # - Demonstrates optimization from O(k log k) to O(k) per word.
    # - Shows awareness of constraints (lowercase English letters).
    #
    # Tradeoff:
    # - Fastest for lowercase a-z input, but less general than sorted-key.
    # - If charset is large/unknown (Unicode), sorted-key is often simpler.
    #
    # Build a fixed-size frequency signature for each word
    # (26 lowercase English letters), and use that signature as the key.
    #
    # Example:
    #   "eat" -> [1,0,0,0,1,...,1,...]
    #   "tea" -> [1,0,0,0,1,...,1,...]  (same counts -> same group)
    #
    # Time complexity (detailed):
    # - For each of n words, we scan each character once -> O(k).
    # - Building the tuple key from 26 counts is O(26) = O(1).
    # - Hash insertion/appending is O(1) average.
    # - Total: O(n * k).
    #
    # Space complexity (detailed):
    # - Output/group storage still holds all words -> O(n * k).
    # - Hashmap keys are tuples of length 26; up to n distinct keys -> O(26 * n) = O(n).
    # - Dominant term remains storing grouped words -> O(n * k).
    # - Total: O(n * k).
    def groupAnagramsCount(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)

        for word in strs:
            count = [0] * 26
            for char in word:
                count[ord(char) - ord("a")] += 1
            groups[tuple(count)].append(word)

        return list(groups.values())


def _normalize(groups: List[List[str]]) -> List[List[str]]:
    return sorted([sorted(group) for group in groups])


# ─────────────────────────────────────────────────────────────
# Tests — run with: python group_anagrams.py
# ─────────────────────────────────────────────────────────────
class TestGroupAnagrams(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = Solution()
        self.expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

    def test_group_anagrams_sorted(self) -> None:
        self.assertEqual(
            _normalize(self.solver.groupAnagramsSorted(["eat", "tea", "tan", "ate", "nat", "bat"])),
            _normalize(self.expected),
        )
        self.assertEqual(_normalize(self.solver.groupAnagramsSorted([""])), [[""]])
        self.assertEqual(_normalize(self.solver.groupAnagramsSorted(["a"])), [["a"]])

    def test_group_anagrams_count(self) -> None:
        self.assertEqual(
            _normalize(self.solver.groupAnagramsCount(["eat", "tea", "tan", "ate", "nat", "bat"])),
            _normalize(self.expected),
        )
        self.assertEqual(_normalize(self.solver.groupAnagramsCount([""])), [[""]])
        self.assertEqual(_normalize(self.solver.groupAnagramsCount(["a"])), [["a"]])

    def test_group_anagrams_default(self) -> None:
        self.assertEqual(
            _normalize(self.solver.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])),
            _normalize(self.expected),
        )
        self.assertEqual(_normalize(self.solver.groupAnagrams([""])), [[""]])
        self.assertEqual(_normalize(self.solver.groupAnagrams(["a"])), [["a"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
    