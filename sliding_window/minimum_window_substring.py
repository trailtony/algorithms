import unittest


class Solution:
    # LeetCode expected method name.
    # In interviews: show baseline first, then route to the optimal approach.
    def minWindow(self, s: str, t: str) -> str:
        return self.minWindowOptimal(s, t)

    # ── APPROACH 1: Brute Force Baseline ───────────────────────────────
    # Interview framing:
    # - Generate all substrings s[i:j].
    # - Check if each substring contains every character from t (with frequency).
    # - Keep the shortest valid one.
    #
    # Why interviewer may like this:
    # - Shows a correct baseline before optimization.
    # - Makes transition to sliding-window optimization explicit.
    #
    # Tradeoff:
    # - Too slow for large inputs.
    #
    # Time complexity:
    # - Outer loop over i: O(n)
    # - Inner loop over j: O(n)
    # - Validate against required map: O(u), where u = unique chars in t
    # - Total: O(n^2 * u), commonly described as O(n^3) in worst case.
    #
    # Space complexity:
    # - count_t + rolling count_s maps: O(u + v)
    # - O(n) worst-case in theory; bounded by charset size in practice.
    def minWindowBrute(self, s: str, t: str) -> str:
        if t == "":
            return ""

        count_t = {}
        for c in t:
            count_t[c] = count_t.get(c, 0) + 1

        best_l, best_r = -1, -1
        best_len = float("infinity")

        for i in range(len(s)):
            count_s = {}
            for j in range(i, len(s)):
                count_s[s[j]] = count_s.get(s[j], 0) + 1

                valid = True
                for c in count_t:
                    if count_s.get(c, 0) < count_t[c]:
                        valid = False
                        break

                if valid and (j - i + 1) < best_len:
                    best_len = j - i + 1
                    best_l, best_r = i, j

        return s[best_l:best_r + 1] if best_len != float("infinity") else ""

    # ── APPROACH 2: Optimal Sliding Window ─────────────────────────────
    # Interview framing:
    # - Keep one window [l..r] that expands rightward.
    # - Track when the window satisfies all required chars from t.
    # - Once valid, shrink from the left to make it minimal.
    #
    # Core invariant:
    # - have == need  <=> current window satisfies all required frequencies.
    #
    # Time complexity:
    # - O(n + m), where n = len(s), m = len(t).
    # - Right pointer moves across s once, left pointer also moves at most once.
    #
    # Space complexity:
    # - O(u + v) for required and current window maps.
    # - O(n) worst-case in theory; bounded by charset size in practice.
    def minWindowOptimal(self, s: str, t: str) -> str:
        if t == "":
            return ""

        count_t, window = {}, {}
        for c in t:
            count_t[c] = count_t.get(c, 0) + 1

        have, need = 0, len(count_t)
        best_l, best_r = -1, -1
        best_len = float("infinity")
        l = 0

        for r in range(len(s)):
            c = s[r]
            window[c] = window.get(c, 0) + 1

            if c in count_t and window[c] == count_t[c]:
                have += 1

            while have == need:
                if (r - l + 1) < best_len:
                    best_l, best_r = l, r
                    best_len = r - l + 1

                left_char = s[l]
                window[left_char] -= 1
                if left_char in count_t and window[left_char] < count_t[left_char]:
                    have -= 1
                l += 1

        return s[best_l:best_r + 1] if best_len != float("infinity") else ""


class TestMinimumWindowSubstring(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = Solution()

    def _assert_all_methods(self, s: str, t: str, expected: str) -> None:
        self.assertEqual(self.solver.minWindowBrute(s, t), expected)
        self.assertEqual(self.solver.minWindowOptimal(s, t), expected)
        self.assertEqual(self.solver.minWindow(s, t), expected)

    def test_standard_example(self) -> None:
        self._assert_all_methods("ADOBECODEBANC", "ABC", "BANC")

    def test_single_character_exact_match(self) -> None:
        self._assert_all_methods("a", "a", "a")

    def test_target_longer_than_source(self) -> None:
        self._assert_all_methods("a", "aa", "")

    def test_empty_target(self) -> None:
        self._assert_all_methods("anything", "", "")

    def test_duplicate_requirements(self) -> None:
        self._assert_all_methods("aaflslflsldkalskaaa", "aaa", "aaa")

    def test_zero_or_more_extra_characters(self) -> None:
        self._assert_all_methods("bba", "ab", "ba")


if __name__ == "__main__":
    unittest.main(verbosity=2)