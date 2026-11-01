"""Top K Frequent Elements (LeetCode 347): sort, min-heap and bucket sort, with complexity analysis, interview notes and tests.

Pattern: Arrays & Hashing (frequency counting), then Top-K selection
(sorting, heap, or bucket sort).

PROBLEM
-------
Given an integer array nums and an integer k, return the k most frequent
elements in any order. LeetCode guarantees the answer is unique, so there
is never a tie at the k-th position.

COMPLEXITY ANALYSIS
-------------------
Let n = len(nums), m = number of distinct values (m <= n), k <= m.

Solution 1, sort the (frequency, value) pairs:
    Time:  O(n + m log m), which is O(n log n) in the worst case. Counting
           is O(n), sorting the m pairs dominates.
    Space: O(m) for the count dict and the list of pairs.

Solution 2, min-heap of size k:
    Time:  O(n + m log k). Counting is O(n). Each of the m distinct values
           is pushed once and at most one value is popped per push, and
           every heap operation costs O(log k).
    Space: O(m + k). The count dict plus a heap that never exceeds k + 1.
    Best choice when k is much smaller than m.

Solution 3, bucket sort by frequency:
    Time:  O(n). Counting is O(n), filling the buckets is O(m), and the
           final scan touches at most n + 1 buckets and m values.
    Space: O(n). The count dict plus n + 1 buckets.
    Fastest in big-O terms, at the cost of allocating n + 1 lists up front.

Alternative worth naming (not implemented here):
    Quickselect on the frequencies: O(n) average, O(n^2) worst case, O(m)
    space. Same idea as the partition step of quicksort.

INTERVIEW QUESTIONS AND PITFALLS
--------------------------------
Q1. Can you beat O(n log n)?
    Yes. A value can appear at most n times, so frequency is a bounded
    integer in 1..n and can be used directly as an array index. That is
    bucket sort and it gives O(n) time with no comparisons.

Q2. Why does the bucket array need n + 1 slots?
    Frequencies range from 1 to n inclusive. Index n must exist for the
    case where every element is the same. Index 0 is never used because
    every counted value appears at least once, so the scan can stop at 1.

Q3. What is the classic bucket sort mistake?
    Using the VALUE as the bucket index instead of the FREQUENCY. Values
    can be negative or huge, frequencies cannot. The bucket index is
    always the count.

Q4. Why is the heap a min-heap when we want the largest frequencies?
    A min-heap of size k keeps the k largest seen so far, and its root is
    the smallest of those k, so it is the one to evict when a better
    candidate arrives. A max-heap would require pushing all m values and
    popping k times, which is O(m log m) and loses the advantage.

Q5. What should the heap store?
    Tuples of (frequency, value). heapq compares tuples element by element,
    so the frequency decides the order. Storing only the value would lose
    the frequency, and storing (value, frequency) would order by value.

Q6. When do you pick the heap over bucket sort?
    When k is much smaller than n. The heap holds only k items and costs
    O(m log k), while bucket sort always allocates n + 1 lists. When k is
    close to m, the log k factor is no longer small and buckets win.

Q7. What do you do about ties at the k-th position?
    LeetCode guarantees a unique answer, so nothing. In a real system you
    must ask for the tie-breaking rule (smaller value first, first seen
    first, or return all tied values) because all three approaches break
    ties arbitrarily or by tuple order.

Q8. What if k is greater than the number of distinct values?
    Outside the constraints. Solution 1 raises IndexError from pop() on an
    empty list. Solutions 2 and 3 return all m values. Ask which behavior
    the caller expects, and state that the constraints rule this out.

Q9. Does the output order matter?
    No, the problem accepts any order. Do not spend time sorting the
    result. Tests must compare as sets or by frequency, not by position.

Q10. Follow-up: what if nums is a stream you cannot store?
     Exact counting needs O(m) memory. For approximate answers use a
     Count-Min Sketch to estimate frequencies in fixed memory with a
     small heap of candidates, or Misra-Gries (heavy hitters) when you
     only need elements above a frequency threshold.

Q11. Follow-up: how would Quickselect apply here?
     Partition the m distinct values by frequency around a pivot until
     the k most frequent sit on one side. O(n) average, but O(n^2) in the
     worst case with bad pivots, which is why the heap or buckets are the
     safer answers in an interview.
"""

import heapq
import random
import unittest
from collections import Counter


class Solution:
    """LeetCode solution container holding the sort, heap and bucket approaches."""

    def topKFrequentSort(self, nums: list[int], k: int) -> list[int]:
        """Return the k most frequent values by sorting (frequency, value) pairs."""
        count: dict[int, int] = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1

        # Tuples sort by frequency first, so the most frequent end up last.
        freq_pairs = sorted((freq, num) for num, freq in count.items())

        res: list[int] = []
        while len(res) < k:
            res.append(freq_pairs.pop()[1])
        return res

    def topKFrequentHeap(self, nums: list[int], k: int) -> list[int]:
        """Return the k most frequent values using a min-heap capped at size k."""
        count = Counter(nums)

        heap: list[tuple[int, int]] = []
        for num, freq in count.items():
            heapq.heappush(heap, (freq, num))
            # Evict the least frequent candidate so the heap never exceeds k.
            if len(heap) > k:
                heapq.heappop(heap)

        return [num for _, num in heap]

    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        """Return the k most frequent values using bucket sort in O(n)."""
        count = Counter(nums)

        # Index is the frequency (0..n), so n + 1 buckets. Index 0 stays empty
        # because every counted value appears at least once.
        buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            buckets[freq].append(num)

        res: list[int] = []
        # Walk from the highest possible frequency down and stop at k values.
        for freq in range(len(buckets) - 1, 0, -1):
            for num in buckets[freq]:
                res.append(num)
                if len(res) == k:
                    return res

        return res


# ---------------------------------------------------------------------------
# Tests (run with: uv run python -m unittest -v top_k_frequent_elements)
# ---------------------------------------------------------------------------

METHODS = ("topKFrequentSort", "topKFrequentHeap", "topKFrequent")


class TestTopKFrequent(unittest.TestCase):
    """Unit tests covering the sort, heap and bucket solutions."""

    # Each case is (nums, k, expected). Compared as sets because order is free.
    KNOWN_CASES: list[tuple[list[int], int, set[int]]] = [
        ([1, 1, 1, 2, 2, 3], 2, {1, 2}),  # LeetCode example 1
        ([1], 1, {1}),  # LeetCode example 2, single element
        ([4, 4, 4, 4], 1, {4}),  # every element identical (bucket index n)
        ([1, 2, 3], 3, {1, 2, 3}),  # k equals the number of distinct values
        ([-1, -1, 0, 0, 0, 5], 2, {-1, 0}),  # negative values and zero (Q3)
        ([1, 2, 2, 3, 3, 3], 1, {3}),  # k = 1 picks the single most frequent
        ([5, 5, 5, 2, 2, 7], 2, {5, 2}),  # unsorted input
        ([1000000, 1000000, -1000000], 1, {1000000}),  # large magnitude values
    ]

    def setUp(self) -> None:
        """Create a fresh Solution instance before each test."""
        self.solution = Solution()

    def test_known_cases(self) -> None:
        """All approaches return the expected set on hand-picked cases."""
        for method in METHODS:
            for nums, k, expected in self.KNOWN_CASES:
                # subTest reports each failing (method, input) pair separately.
                with self.subTest(method=method, nums=nums, k=k):
                    result = getattr(self.solution, method)(list(nums), k)
                    self.assertEqual(len(result), k)
                    self.assertEqual(set(result), expected)

    def test_random_inputs_return_valid_top_k(self) -> None:
        """On random inputs the result has k distinct values with the top-k frequencies."""
        rng = random.Random(42)  # fixed seed keeps failures reproducible

        for _ in range(300):
            nums = [rng.randint(-5, 5) for _ in range(rng.randint(1, 40))]
            count = Counter(nums)
            k = rng.randint(1, len(count))
            # Ties at the boundary make the exact values ambiguous, so compare
            # the multiset of frequencies instead of the values themselves.
            expected_freqs = sorted((f for _, f in count.most_common(k)), reverse=True)

            for method in METHODS:
                with self.subTest(method=method, nums=nums, k=k):
                    result = getattr(self.solution, method)(list(nums), k)
                    self.assertEqual(len(result), k)
                    self.assertEqual(len(set(result)), k)  # no duplicates
                    self.assertTrue(set(result) <= set(nums))  # only real values
                    got_freqs = sorted((count[v] for v in result), reverse=True)
                    self.assertEqual(got_freqs, expected_freqs)

    def test_does_not_mutate_input(self) -> None:
        """No approach may modify the caller's list."""
        nums = [1, 1, 1, 2, 2, 3]
        snapshot = list(nums)
        for method in METHODS:
            with self.subTest(method=method):
                getattr(self.solution, method)(nums, 2)
                self.assertEqual(nums, snapshot)


if __name__ == "__main__":
    unittest.main()
