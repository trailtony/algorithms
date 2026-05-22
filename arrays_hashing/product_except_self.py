# ─────────────────────────────────────────────────────────────
# PRODUCT OF ARRAY EXCEPT SELF
# https://leetcode.com/problems/product-of-array-except-self/
# Difficulty: Medium
# ─────────────────────────────────────────────────────────────
#
# PROBLEM
# Given an integer array nums, return an array answer such that
# answer[i] is the product of all elements of nums except nums[i].
#
# Constraints:
#   - Must run in O(n) time
#   - Must not use division
#   - The product of any prefix or suffix fits in a 32-bit integer
#
# Example:
#   nums = [1, 2, 3, 4]  → [24, 12, 8, 6]
#   nums = [-1, 1, 0,-3, 3] → [0, 0, 9, 0, 0]
#
# ┌──────────────────────────────────┬────────────┬────────────┐
# │ Approach                         │ Time       │ Space      │
# ├──────────────────────────────────┼────────────┼────────────┤
# │ Brute force (nested loops)       │ O(n²)      │ O(1)       │
# │ Optimal (prefix + postfix pass)  │ O(n)       │ O(1)*      │
# └──────────────────────────────────┴────────────┴────────────┘
# * O(1) extra space — the output array is not counted per the
#   problem statement since it is required as the return value.
# ─────────────────────────────────────────────────────────────

from typing import List
import unittest


class Solution:
    # LeetCode expected method name (uses optimal approach)
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        return self.productExceptSelfPrefixPostfix(nums)

    # ── APPROACH 1: Brute Force (Nested Loops) ───────────────────
    # Interview framing:
    # - For each index i, compute the product of all nums[j] where j != i.
    # - This is the most direct "definition-first" implementation.
    #
    # Why interviewer may like this:
    # - Shows clear baseline thinking before optimization.
    # - Easy to prove correctness because it mirrors the problem statement.
    #
    # Tradeoff:
    # - Too slow for constraints due to repeated full scans per index.
    #
    # For each position i, multiply every element except nums[i].
    # The inner loop skips index i using a simple if check.
    #
    # Straightforward but expensive — for every element we scan
    # the entire array again, giving us n * n multiplications.
    #
    # Time:  O(n²) — outer loop runs n times, inner loop runs n-1 times
    # Space: O(1)  — only the output array, no extra data structures
    def productExceptSelfBrute(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n
        for i in range(n):
            for j in range(n):
                if i != j:
                    answer[i] *= nums[j]
        return answer

    # ── APPROACH 2: Prefix + Postfix Pass (Optimal) ──────────────
    # Interview framing:
    # - Replace repeated multiplication with pre-aggregated products.
    # - answer[i] should be (all left values) * (all right values).
    # - Compute left products in one pass, right products in one reverse pass.
    #
    # Why interviewer may like this:
    # - Demonstrates turning O(n²) baseline into O(n) with clean logic.
    # - Satisfies both key constraints: no division and O(n) time.
    #
    # Tradeoff:
    # - Slightly less obvious than brute force, but still very readable.
    # - Requires careful pass ordering to avoid overwriting needed state.
    #
    # Key insight: answer[i] = (product of everything LEFT of i)
    #                        × (product of everything RIGHT of i)
    #
    # We compute both sides in two separate passes over the array,
    # storing results directly into the output array — no division,
    # no extra arrays needed.
    #
    # PASS 1 — Left to right (prefix):
    #   answer[i] holds the product of all elements to the LEFT of i.
    #   We start with prefix = 1 (nothing to the left of index 0).
    #   Before storing, we write the current prefix into answer[i],
    #   then multiply prefix by nums[i] for the next iteration.
    #
    #   nums   = [ 1,  2,  3,  4]
    #   prefix:    1   1   2   6     ← product of everything before i
    #   answer = [ 1,  1,  2,  6]   ← after pass 1
    #
    # PASS 2 — Right to left (postfix):
    #   We now multiply each answer[i] by the product of everything
    #   to the RIGHT of i, accumulated in postfix.
    #   We start with postfix = 1 (nothing to the right of last index).
    #
    #   postfix:   24  12  4   1     ← product of everything after i
    #   answer = [ 24, 12, 8,  6]   ← after pass 2 (final answer)
    #
    # Each position ends up as prefix_left × postfix_right = answer[i].
    #
    # Time:  O(n) — two separate single passes over the array
    # Space: O(1) — prefix and postfix are single integer variables.
    #               The output array is excluded per problem constraints.
    def productExceptSelfPrefixPostfix(self, nums: List[int]) -> List[int]:
        n = len(nums)
        answer = [1] * n

        # Pass 1: fill answer[i] with the product of everything left of i
        prefix = 1
        for i in range(n):
            answer[i] = prefix
            prefix *= nums[i]

        # Pass 2: multiply answer[i] by the product of everything right of i
        postfix = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= postfix
            postfix *= nums[i]

        return answer


# ─────────────────────────────────────────────────────────────
# Tests — run with: python product_except_self.py
# ─────────────────────────────────────────────────────────────
class TestProductExceptSelf(unittest.TestCase):
    def setUp(self) -> None:
        self.solver = Solution()

    def test_product_except_self_brute(self) -> None:
        self.assertEqual(self.solver.productExceptSelfBrute([1, 2, 3, 4]), [24, 12, 8, 6])
        self.assertEqual(self.solver.productExceptSelfBrute([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])
        self.assertEqual(self.solver.productExceptSelfBrute([3, 4]), [4, 3])
        self.assertEqual(self.solver.productExceptSelfBrute([-1, -2, -3, -4]), [-24, -12, -8, -6])
        self.assertEqual(self.solver.productExceptSelfBrute([0, 0]), [0, 0])

    def test_product_except_self_prefix_postfix(self) -> None:
        self.assertEqual(self.solver.productExceptSelfPrefixPostfix([1, 2, 3, 4]), [24, 12, 8, 6])
        self.assertEqual(self.solver.productExceptSelfPrefixPostfix([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])
        self.assertEqual(self.solver.productExceptSelfPrefixPostfix([3, 4]), [4, 3])
        self.assertEqual(self.solver.productExceptSelfPrefixPostfix([-1, -2, -3, -4]), [-24, -12, -8, -6])
        self.assertEqual(self.solver.productExceptSelfPrefixPostfix([0, 0]), [0, 0])

    def test_product_except_self_default(self) -> None:
        self.assertEqual(self.solver.productExceptSelf([1, 2, 3, 4]), [24, 12, 8, 6])
        self.assertEqual(self.solver.productExceptSelf([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])
        self.assertEqual(self.solver.productExceptSelf([3, 4]), [4, 3])
        self.assertEqual(self.solver.productExceptSelf([-1, -2, -3, -4]), [-24, -12, -8, -6])
        self.assertEqual(self.solver.productExceptSelf([0, 0]), [0, 0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
