from collections import defaultdict
from typing import List
import random
import unittest
# Why these imports:
# - defaultdict(list): creates an empty list for a new key automatically,
#   so grouping logic can append directly without manual key checks.
# - List: adds clear type hints for inputs/outputs, improving readability
#   and helping static analyzers/editors catch type issues early.
# - random: seeded random inputs for the sorted-vs-count cross-check test.


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
#
# ─────────────────────────────────────────────────────────────
# INTERVIEW QUESTIONS AND PITFALLS
# ─────────────────────────────────────────────────────────────
#
# Q1. Why does a sorted word work as a grouping key?
#     Two strings are anagrams exactly when they contain the same multiset
#     of characters. Sorting turns that multiset into one canonical string,
#     so equal keys mean anagrams and different keys mean not anagrams.
#
# Q2. Why is the count key a tuple and not a list?
#     A dict key must be hashable. A list is mutable and unhashable, so
#     groups[count] raises TypeError. tuple(count) is immutable and hashable.
#
# Q3. What is the pitfall when building a string key from the counts?
#     Joining the counts without a separator is ambiguous. Counts [1, 11]
#     and [11, 1] both become "111". If you use a string key, put a
#     separator between the counts (for example "#"). A tuple avoids the
#     problem entirely.
#
# Q4. What breaks the count approach outside lowercase a-z?
#     The index is ord(c) - ord("a"), and Python lists accept negative
#     indices. Characters from "G" to "`" produce an index in -26..-1 that
#     wraps around instead of failing, so "Z" lands in the slot of "t" and
#     "`" lands in the slot of "z". Words like "Z" and "t" are then grouped
#     as anagrams with no error. Characters below "G" (including "A" to "F")
#     raise IndexError, and characters above "z" also raise IndexError.
#     The silent wraparound is the dangerous case. State the lowercase
#     assumption before you write the code.
#
# Q5. Which approach do you present first in an interview?
#     The sorted key. It is three lines, works for any characters, and is
#     easy to get right. Then offer the count key as the optimization from
#     O(k log k) to O(k) per word, and say the lowercase constraint out loud.
#
# Q6. Is the O(k) count key always faster than the O(k log k) sorted key?
#     Not in practice for short words. sorted() runs at C speed while the
#     count loop runs in Python bytecode, so the asymptotically worse
#     version is often faster on typical short inputs. The count key wins
#     as k grows. Measure with timeit before claiming either is better.
#
# Q7. How do you handle arbitrary Unicode with a linear-time key?
#     Use a frequency map as the key: frozenset(Counter(word).items()).
#     It is hashable, takes O(k) to build, and works for any characters.
#     Sorting the items into a tuple also works, at O(k + d log d) where d
#     is the number of distinct characters.
#
# Q8. What edge cases do you test?
#     An empty list (returns []), [""] (one group with the empty string),
#     several empty strings (one group), a single word, duplicates
#     ("a", "a" form one group), all words anagrams of each other (one
#     group), and no anagrams at all (n groups of one).
#
# Q9. Does the output order matter?
#     No. Both the order of the groups and the order inside each group are
#     free, so tests must normalize (sort) before comparing.
#
# Q10. Why does the dict use defaultdict(list) and not a plain dict?
#      With a plain dict, groups[key].append(word) raises KeyError the first
#      time a key appears, because there is no list to append to yet.
#      defaultdict(list) creates the empty list on first access. The plain
#      dict alternative is groups.setdefault(key, []).append(word).
#
# Q11. Follow-up: what if the list of words is too large for one machine?
#      The key already tells you where a word belongs. Hash the key and
#      send every word with the same key to the same worker, then group
#      locally. This is the shuffle step of a map-reduce job.



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
    def groupAnagramsCount(self, strs: list[str]) -> list[list[str]]:
        groups = defaultdict(list)

        for word in strs:
            count = [0] * 26
            for char in word:
                count[ord(char) - ord("a")] += 1
            groups[tuple(count)].append(word)

        return list(groups.values())


def _normalize(groups: list[list[str]]) -> list[list[str]]:
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


class TestGroupAnagramsEdgeCases(unittest.TestCase):
    """Edge cases (Q8), cross-check between approaches, and the Q4 pitfall."""

    METHODS = ("groupAnagramsSorted", "groupAnagramsCount", "groupAnagrams")

    # Each case is (input, expected groups). Compared after normalizing.
    EDGE_CASES: List[tuple[List[str], List[List[str]]]] = [
        ([], []),  # empty list
        (["", ""], [["", ""]]),  # several empty strings form one group
        (["a", "a"], [["a", "a"]]),  # duplicates form one group
        (["abc", "bca", "cab"], [["abc", "bca", "cab"]]),  # all anagrams
        (["a", "b", "c"], [["a"], ["b"], ["c"]]),  # no anagrams at all
        (["ab", "abc"], [["ab"], ["abc"]]),  # same letters, different lengths
        (["aab", "aba", "abb"], [["aab", "aba"], ["abb"]]),  # same letters, different counts
    ]

    def setUp(self) -> None:
        self.solver = Solution()

    def test_edge_cases(self) -> None:
        for method in self.METHODS:
            for strs, expected in self.EDGE_CASES:
                # subTest reports each failing (method, input) pair separately.
                with self.subTest(method=method, strs=strs):
                    result = getattr(self.solver, method)(list(strs))
                    self.assertEqual(_normalize(result), _normalize(expected))

    def test_sorted_and_count_agree_on_random_lowercase_input(self) -> None:
        rng = random.Random(42)  # fixed seed keeps failures reproducible

        for _ in range(300):
            strs = [
                "".join(rng.choice("abc") for _ in range(rng.randint(0, 5)))
                for _ in range(rng.randint(0, 12))
            ]
            with self.subTest(strs=strs):
                self.assertEqual(
                    _normalize(self.solver.groupAnagramsSorted(list(strs))),
                    _normalize(self.solver.groupAnagramsCount(list(strs))),
                )

    def test_sorted_key_handles_uppercase_and_unicode(self) -> None:
        strs = ["Ab", "bA", "ab", "日本", "本日"]
        expected = [["Ab", "bA"], ["ab"], ["日本", "本日"]]
        self.assertEqual(
            _normalize(self.solver.groupAnagramsSorted(strs)), _normalize(expected)
        )

    def test_count_key_silently_conflates_wraparound_characters(self) -> None:
        # Documents the Q4 pitfall: this is WRONG behavior, kept as a warning.
        # "Z" (index -7) wraps to the slot of "t", so these are grouped together.
        result = self.solver.groupAnagramsCount(["Z", "t"])
        self.assertEqual(_normalize(result), [["Z", "t"]])

    def test_count_key_raises_on_out_of_range_characters(self) -> None:
        # "A" gives index -32, which is outside -26..-1, so IndexError (Q4).
        with self.assertRaises(IndexError):
            self.solver.groupAnagramsCount(["A"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
