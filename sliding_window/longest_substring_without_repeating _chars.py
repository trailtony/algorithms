"""Longest Substring Without Repeating Characters (LeetCode 3): brute force, sliding window with a set, and sliding window with last-seen indices, with complexity analysis, interview notes and tests.

Pattern: Sliding Window (variable size, shrink when the window becomes invalid).

PROBLEM
-------
Given a string s, return the length of the longest substring that contains
no repeated characters. A substring is contiguous, unlike a subsequence.

THE IDEA
--------
Keep a window s[l..r] that never contains a duplicate. Move r forward one
character at a time. If s[r] is already inside the window, move l forward
until the duplicate has left the window. After the window is valid again,
its length r - l + 1 is a candidate for the answer.

COMPLEXITY ANALYSIS
-------------------
Let n = len(s) and m = size of the alphabet (for example 128 for ASCII).

Solution 1, brute force with early break:
    Time:  O(n^2) in the worst case. For every start index we extend until
           the first repeat. Each inner scan is bounded by min(n, m), so
           the exact bound is O(n * min(n, m)).
    Space: O(min(n, m)) for the set of seen characters.

Solution 2, sliding window with a set (the interview-facing answer):
    Time:  O(n). The nested loop looks quadratic but is not: r moves
           forward n times in total, and l only ever moves forward and
           never passes r, so it also moves at most n times. Every
           character is added to the set once and removed at most once,
           so the total work is at most 2n set operations.
    Space: O(min(n, m)). The set never holds more than one copy of each
           distinct character, and never more than n characters.

Solution 3, sliding window with last-seen indices:
    Time:  O(n). One pass with no inner loop. When a repeat is found, l
           jumps directly past the previous occurrence instead of
           stepping one character at a time.
    Space: O(min(n, m)). The dict holds one entry per distinct character
           seen. Keys are never removed.

INTERVIEW QUESTIONS AND PITFALLS
--------------------------------
Q1. What is the invariant of the window?
    s[l..r] never contains a repeated character. Every step either extends
    the window (when s[r] is new) or shrinks it from the left until the
    invariant holds again. The answer is the largest window length seen.

Q2. Why is the shrinking step a while loop and not an if?
    The duplicate of s[r] can be anywhere inside the window, so several
    characters may have to leave before it does. In "abcdb" with r on the
    second "b", l must move past "a" and the first "b", which is two
    removals. An if removes only one character and leaves the window
    invalid.

Q3. The code has a loop inside a loop. Why is it O(n) and not O(n^2)?
    Because l never moves backward. Across the entire run, r advances n
    times and l advances at most n times, so the inner while loop runs at
    most n times in total, not n times per iteration. This is amortized
    analysis, and it is the question interviewers ask about this problem
    most often.

Q4. Why is the space O(min(n, m)) and not O(n)?
    The set holds distinct characters only, and it cannot hold more
    characters than the string has or than the alphabet contains. For
    lowercase letters or ASCII it is O(1) in practice. State the alphabet
    assumption before you claim O(1).

Q5. What is the difference between a substring and a subsequence?
    A substring is contiguous and a subsequence is not. For "pwwkew" the
    answer is 3 ("wke"). "pwke" has length 4 but is a subsequence, so it
    does not count.

Q6. What is the classic bug in the last-seen-index version?
    Forgetting to check that the previous occurrence is inside the current
    window. Without the check last[c] >= l, l can move backward. For
    "abba", at the final "a" the stored index is 0, which is left of
    l = 2. Setting l = 0 + 1 = 1 re-includes the second "b" in the window
    and returns 3 instead of 2. The map is never cleaned, so stale
    indices are expected and must be ignored.

Q7. When do you update the result, before or after shrinking?
    After. The window is only valid once the duplicate has been removed
    and s[r] has been added. Measuring before shrinking counts an invalid
    window.

Q8. Which version do you present first?
    The set version. Its invariant is easy to say out loud and easy to
    get right on a whiteboard. Then mention that the last-seen-index
    version removes the inner loop by jumping l, with the same O(n) time.

Q9. What edge cases do you test?
    The empty string (0), a single character (1), all characters equal
    ("bbbbb" gives 1), all characters distinct (the whole string), a
    repeat at the very end, the "abba" case from Q6, "dvdf" (the answer
    does not start at index 0), spaces and symbols, and non-ASCII text.

Q10. Follow-up: return the substring itself instead of the length.
     Track the start index of the best window: whenever r - l + 1 beats
     the current best, save l as best_start. Return s[best_start:
     best_start + best_len]. Same complexity.

Q11. Follow-up: at most k distinct characters (LeetCode 340, or 159 for k = 2).
     Same window, but replace the set with a dict of character counts and
     shrink while len(counts) > k. A set cannot be used because removing
     one copy of a character must not drop it while other copies remain.

Q12. Which related problems use the same pattern?
     Longest Repeating Character Replacement, Permutation in String and
     Minimum Window Substring. All keep a window, extend with r, and
     shrink with l when a condition fails.

Q13. Does Python's len(s) match the characters a user sees?
     Python strings are sequences of code points, so a character built
     from several code points (an accent written as a combining mark, or
     some emoji) counts as more than one. The algorithm is correct for
     code points. Ask the interviewer whether grapheme clusters matter.
"""

import random
import unittest


class Solution:
    """LeetCode solution container holding brute force and two sliding window approaches."""

    def lengthOfLongestSubstringBruteForce(self, s: str) -> int:
        """Return the longest unique substring length by extending from every start index."""
        res = 0

        for i in range(len(s)):
            seen: set[str] = set()
            for j in range(i, len(s)):
                if s[j] in seen:
                    break
                seen.add(s[j])
                res = max(res, j - i + 1)

        return res

    def lengthOfLongestSubstring(self, s: str) -> int:
        """Return the longest unique substring length using a sliding window and a set."""
        res = 0
        l = 0
        char_set: set[str] = set()

        for r in range(len(s)):
            # A while loop is required: the duplicate may sit anywhere in the
            # window, so several characters may have to leave (see Q2).
            while s[r] in char_set:
                char_set.remove(s[l])
                l += 1
            char_set.add(s[r])
            res = max(res, r - l + 1)

        return res

    def lengthOfLongestSubstringLastIndex(self, s: str) -> int:
        """Return the longest unique substring length using a sliding window that jumps l."""
        res = 0
        l = 0
        last_seen: dict[str, int] = {}

        for r, c in enumerate(s):
            # Only jump if the previous occurrence is inside the window (see Q6).
            # Stale indices left of l must be ignored, never used to move l back.
            if c in last_seen and last_seen[c] >= l:
                l = last_seen[c] + 1
            last_seen[c] = r
            res = max(res, r - l + 1)

        return res


# ---------------------------------------------------------------------------
# Tests (run with: uv run python -m unittest -v longest_substring_without_repeating_characters)
# ---------------------------------------------------------------------------

METHODS = (
    "lengthOfLongestSubstringBruteForce",
    "lengthOfLongestSubstring",
    "lengthOfLongestSubstringLastIndex",
)


class TestLengthOfLongestSubstring(unittest.TestCase):
    """Unit tests covering brute force and both sliding window solutions."""

    # Each case is (s, expected_length).
    KNOWN_CASES: list[tuple[str, int]] = [
        ("abcabcbb", 3),  # LeetCode example 1
        ("bbbbb", 1),  # LeetCode example 2, all characters equal
        ("pwwkew", 3),  # LeetCode example 3, substring not subsequence (Q5)
        ("", 0),  # empty string
        (" ", 1),  # single space
        ("a", 1),  # single character
        ("au", 2),  # two distinct characters
        ("abcdef", 6),  # all distinct, the whole string
        ("aab", 2),  # repeat at the start
        ("dvdf", 3),  # best window does not start at index 0
        ("abba", 2),  # stale index trap for the last-seen version (Q6)
        ("tmmzuxt", 5),  # stale index trap with a later repeat
        ("abcdb", 4),  # "abcd" wins, and the final b needs two removals (Q2)
        ("1231234", 4),  # digits, best window at the end
        ("a b c", 3),  # spaces count as characters
        ("日本語日", 3),  # non-ASCII code points
    ]

    def setUp(self) -> None:
        """Create a fresh Solution instance before each test."""
        self.solution = Solution()

    def test_known_cases(self) -> None:
        """All approaches return the expected length on hand-picked cases."""
        for method in METHODS:
            for s, expected in self.KNOWN_CASES:
                # subTest reports each failing (method, input) pair separately.
                with self.subTest(method=method, s=s):
                    self.assertEqual(getattr(self.solution, method)(s), expected)

    def test_sliding_windows_match_brute_force_on_random_inputs(self) -> None:
        """Both sliding window versions agree with brute force on many random strings."""
        rng = random.Random(42)  # fixed seed keeps failures reproducible
        alphabet = "abcd "  # small alphabet forces many repeats

        for _ in range(500):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 20)))
            expected = self.solution.lengthOfLongestSubstringBruteForce(s)
            with self.subTest(s=s):
                self.assertEqual(self.solution.lengthOfLongestSubstring(s), expected)
                self.assertEqual(self.solution.lengthOfLongestSubstringLastIndex(s), expected)

    def test_result_never_exceeds_distinct_character_count(self) -> None:
        """The answer can never be larger than the number of distinct characters."""
        rng = random.Random(7)

        for _ in range(200):
            s = "".join(rng.choice("abc") for _ in range(rng.randint(0, 15)))
            for method in METHODS:
                with self.subTest(method=method, s=s):
                    self.assertLessEqual(getattr(self.solution, method)(s), len(set(s)))


if __name__ == "__main__":
    unittest.main()