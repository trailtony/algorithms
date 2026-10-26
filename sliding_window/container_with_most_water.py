"""Container With Most Water (LeetCode 11): brute force vs two pointers, with interview notes and tests.

Pattern: Two Pointers (opposite ends, greedy pointer movement).

INTERVIEW QUESTIONS (answer out loud before reading the code)
-------------------------------------------------------------
Q1. What is the area formula and what are the two competing forces?
    Area = width * min(left_height, right_height). Moving a pointer inward
    always shrinks width by 1, so the only way to beat the current best is
    to find a taller limiting wall.

Q2. Why is it safe to move the pointer at the SHORTER wall?
    Assume l < r and height[l] <= height[r]. Then area(l, r) = (r - l) *
    height[l]. Take any k with l < k < r. The pair (l, k) has width k - l,
    which is smaller than r - l, and height min(height[l], height[k]),
    which is at most height[l]. So area(l, k) <= area(l, r). Every other
    pair that contains l is therefore no better than (l, r), which has
    just been measured. Wall l can be discarded without losing the optimum.

Q3. What happens when the two heights are equal?
    The condition in Q2 holds for both walls, because height[l] ==
    height[r] satisfies height[l] <= height[r] and height[r] <= height[l].
    Discarding either one is safe. The code discards r.

Q4. Time and space complexity of each approach?
    Brute force: O(n^2) time, O(1) space. Two pointers: O(n) time, O(1)
    space, because each iteration moves one pointer and they never cross.

Q5. Does the water "overflow" or get blocked by walls in between?
    No. The problem only cares about the two lines forming the container;
    the lines between them are ignored.

Q6. What edge cases do you test?
    Fewer than two lines (area 0), all zeros, equal heights, strictly
    increasing, strictly decreasing, and a tall pair far apart with short
    lines in between.

Q7. Follow-up: how does this differ from Trapping Rain Water?
    Trapping Rain Water counts water held BETWEEN all bars (the in-between
    bars matter), while this problem picks just two bars. Trapping Rain
    Water also uses two pointers but tracks left_max and right_max.

Q8. Follow-up: can you prove the greedy is correct?
    Loop invariant: res is >= the area of every pair that has at least one
    index outside the window [l, r].
    Initially the window is the whole array, so no pair is outside it and
    the invariant holds.
    Step: the loop measures (l, r) and updates res. It then discards the
    wall with the smaller height. By Q2, every remaining pair containing
    that wall has area <= area(l, r) <= res. So the invariant holds for
    the new, smaller window.
    Termination: when l == r the window contains no pair, so res is >= the
    area of every pair in the array. res is the maximum.
"""

import random
import unittest

class Solution:
    def maxAreaBruteForce(self, height: list[int]) -> int:
        #BRUTE FORCE: O(n) * O(n-1) = O(n^2)
        res = 0
        
        for l in range(len(height)):
            for r in range(l+1, len(height)):
                area = (r - l) * min(height[l], height[r])
                res = max(res, area)
        
        return res
    
    def maxArea(self, height: list[int]):
        #TWO POINTERS: LINEAR TIME O(n)
        res = 0
        l, r = 0, len(height) - 1
        
        while l < r:
            area = (r - l) * min(height[l], height[r])
            res = max(res, area)
            
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        
        return res

# ---------------------------------------------------------------------------
# Tests (run with: uv run python -m unittest -v container_with_most_water)
# ---------------------------------------------------------------------------


class TestMaxArea(unittest.TestCase):
    """Unit tests covering both the brute force and two-pointer solutions."""

    # Each case is (height, expected_area).
    KNOWN_CASES: list[tuple[list[int], int]] = [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),  # LeetCode example 1
        ([1, 1], 1),  # LeetCode example 2, minimum valid input
        ([], 0),  # empty input
        ([5], 0),  # single line cannot hold water
        ([0, 0, 0, 0], 0),  # all zero heights
        ([4, 4, 4, 4], 12),  # equal heights, widest pair wins
        ([1, 2, 3, 4, 5], 6),  # strictly increasing
        ([5, 4, 3, 2, 1], 6),  # strictly decreasing
        ([10, 1, 1, 1, 10], 40),  # tall pair far apart, short lines between
        ([2, 3, 4, 5, 18, 17, 6], 17),  # best pair is not the widest
    ]

    def setUp(self) -> None:
        """Create a fresh Solution instance before each test."""
        self.solution = Solution()

    def test_known_cases(self) -> None:
        """Both approaches return the expected area on hand-picked cases."""
        for method in ("maxAreaBruteForce", "maxArea"):
            for height, expected in self.KNOWN_CASES:
                # subTest reports each failing (method, input) pair separately
                # instead of stopping at the first failure.
                with self.subTest(method=method, height=height):
                    self.assertEqual(getattr(self.solution, method)(height), expected)

    def test_two_pointers_matches_brute_force_on_random_inputs(self) -> None:
        """The optimized solution agrees with brute force on many random arrays."""
        rng = random.Random(42)  # fixed seed keeps failures reproducible

        for _ in range(500):
            height = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
            with self.subTest(height=height):
                self.assertEqual(
                    self.solution.maxArea(height),
                    self.solution.maxAreaBruteForce(height),
                )

    def test_does_not_mutate_input(self) -> None:
        """The solution must leave the input list untouched."""
        height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        snapshot = list(height)
        self.solution.maxArea(height)
        self.assertEqual(height, snapshot)

if __name__ == "__main__":
    unittest.main()