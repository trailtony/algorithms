"""Second Highest Salary (LeetCode 176, pandas): sort, max-below-max and dense rank, with complexity analysis, interview notes and tests.

Pattern: "Nth highest" selection over distinct values, plus the requirement
that the result is ALWAYS a one-row DataFrame, holding None when no second
highest salary exists.

PROBLEM
-------
Given a DataFrame employee with columns id (int, primary key) and salary
(int), return a one-row DataFrame with a single column named
SecondHighestSalary holding the second highest DISTINCT salary, or None if
there is none.

Example 1: salaries 100, 200, 300  ->  200
Example 2: salaries 100            ->  None

HOW TO RUN
----------
    uv add pandas
    uv run python -m unittest -v second_highest_salary_pandas
To submit on LeetCode, copy only the function you want (together with the
_to_result helper if it uses it) and keep the name second_highest_salary.

THE TWO TRAPS
-------------
1. Duplicates: salaries 300, 300, 200 have second highest 200, not 300.
2. The result shape: returning a bare number, an empty DataFrame, or NaN
   instead of None fails. The answer is always a one-row DataFrame, and the
   missing case holds None. The SQL version needed a wrapper query for the
   same reason; here the helper _to_result plays that role.

COMPLEXITY ANALYSIS
-------------------
Let n = number of rows and d = number of distinct salaries (d <= n).

Solution 1, drop duplicates, sort, take position 1:
    Time:  O(n + d log d), which is O(n log n) in the worst case.
    Space: O(n). dropna and drop_duplicates create new Series.

Solution 2, maximum of the salaries strictly below the maximum:
    Time:  O(n). Two vectorized passes (max, then filter and max).
    Space: O(n). Unlike SQL, pandas materializes the boolean mask and the
           filtered Series, so this is not O(1) here.

Solution 3, dense rank, keep rank 2:
    Time:  O(n log n). rank sorts the values.
    Space: O(n). A rank Series the size of the input.

Alternative worth naming (not implemented here):
    salary.drop_duplicates().nlargest(2): O(n log 2), effectively O(n), and
    nlargest ignores NaN. Take .iloc[-1] only when it returned 2 values.

INTERVIEW QUESTIONS AND PITFALLS
--------------------------------
Q1. Why must the function return a DataFrame and not a number?
    The problem specifies a result table with a column named
    SecondHighestSalary. The grader compares a DataFrame, so a scalar,
    a Series or a differently named column fails even when the value is
    right. The column name is case-sensitive.

Q2. None or NaN for the missing case?
    The problem says None. pd.DataFrame({"x": [None]}) keeps None in an
    object column, while float NaN would give a float column. _to_result
    converts any missing value (NaN from an empty max, or None) with
    pd.isna, so every solution returns the same thing.

Q3. What breaks Solution 1 if you skip the length guard?
    distinct.iloc[1] raises IndexError when there are fewer than two
    distinct salaries (one salary, all equal, or an empty table). The
    guard len(distinct) >= 2 turns that case into None.

Q4. Why is drop_duplicates needed in Solution 1?
    Without it, sorted 300, 300, 200 puts 300 at position 1, which is the
    highest again. Distinct values must be sorted, not rows.

Q5. How does Solution 2 avoid needing drop_duplicates?
    It filters with salary < max, which removes every copy of the top
    salary at once. The maximum of what remains is the second highest
    distinct value, whatever the duplicates.

Q6. How does Solution 2 produce None on empty input without a branch?
    Series.max() on an empty Series (or one where the filter kept
    nothing) returns NaN instead of raising, and _to_result maps NaN to
    None. This is the pandas version of "MAX over zero rows is NULL" in SQL.

Q7. Which rank method is correct and why?
    method="dense" is the only correct one. With 300, 300, 200, the
    default method="average" gives 1.5, 1.5, 3, so no value ranks 2.
    method="min" (the SQL RANK) gives 1, 1, 3 and "first" (the SQL
    ROW_NUMBER) gives 1, 2, 3, which wrongly returns 300. Dense ranking
    gives 1, 1, 2, so rank 2 is 200.

Q8. How does pandas treat NaN salaries compared with PostgreSQL?
    sort_values puts NaN last by default (na_position="last"), the
    opposite of PostgreSQL where NULL sorts first on DESC. max() skips NaN
    by default, and rank leaves NaN as NaN. Solution 1 drops NaN
    explicitly, so it is safe, but you should still say so out loud.

Q9. Why can the returned value be 200.0 instead of 200?
    An integer column that contains NaN is stored as float64, so the
    answer comes back as a float. The value is still equal to 200, and
    LeetCode's input has no NaN. Convert the column to the nullable
    "Int64" dtype if you must keep integers with missing values.

Q10. Why must the input DataFrame not be modified?
     Calling sort_values(inplace=True) or adding a rank column to employee
     changes the caller's data. Work on derived Series, as all three
     solutions do. The tests check that the input is unchanged.

Q11. Follow-up: how do you get the Nth highest salary?
     Solution 1: distinct.iloc[n - 1] with the guard len(distinct) >= n.
     Solution 3: rank == n. Solution 2 does not generalize, because it
     would need n nested max-below-max steps.

Q12. Follow-up: the second highest salary per department?
     Rank inside each group:
     employee.groupby("department")["salary"].rank(method="dense",
     ascending=False) == 2. This is the same pattern as LeetCode 185,
     Department Top Three Salaries, and only Solution 3 extends cleanly.

Q13. Why is Solution 2 O(n) space here but O(1) in the SQL version?
     A database aggregate streams through the rows. pandas builds a full
     boolean mask and a filtered copy in memory, so the extra space grows
     with n.
"""

import random
import unittest

import pandas as pd


def _to_result(value: object) -> pd.DataFrame:
    """Wrap a scalar in the one-row result frame, mapping any missing value to None."""
    return pd.DataFrame({"SecondHighestSalary": [None if pd.isna(value) else value]})


def second_highest_salary_sorted(employee: pd.DataFrame) -> pd.DataFrame:
    """Return the second highest distinct salary by sorting the distinct values."""
    distinct = employee["salary"].dropna().drop_duplicates().sort_values(ascending=False)
    # Guard required: iloc[1] raises IndexError with fewer than two distinct values (Q3).
    return _to_result(distinct.iloc[1] if len(distinct) >= 2 else None)


def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    """Return the second highest distinct salary as the maximum of values below the maximum."""
    salary = employee["salary"]
    # Strictly below the maximum removes every duplicate of the top salary (Q5).
    below_max = salary[salary < salary.max()]
    # max() of an empty Series is NaN, which _to_result turns into None (Q6).
    return _to_result(below_max.max())


def second_highest_salary_dense_rank(employee: pd.DataFrame) -> pd.DataFrame:
    """Return the second highest distinct salary using a dense rank, keeping rank 2."""
    # method="dense" gives ties the same rank and leaves no gaps (Q7).
    ranks = employee["salary"].rank(method="dense", ascending=False)
    # Change "== 2" to "== n" for the Nth highest (Q11).
    return _to_result(employee.loc[ranks == 2, "salary"].max())


# ---------------------------------------------------------------------------
# Tests (run with: uv run python -m unittest -v second_highest_salary_pandas)
# ---------------------------------------------------------------------------

SOLUTIONS = (
    second_highest_salary_sorted,
    second_highest_salary,
    second_highest_salary_dense_rank,
)


def make_employee(salaries: list[int | None]) -> pd.DataFrame:
    """Build an Employee frame, using float64 only when a salary is missing (Q9)."""
    dtype = "float64" if None in salaries else "int64"
    return pd.DataFrame(
        {
            "id": pd.Series(range(1, len(salaries) + 1), dtype="int64"),
            "salary": pd.Series(salaries, dtype=dtype),
        }
    )


def reference(salaries: list[int | None]) -> int | None:
    """Return the expected answer with plain Python, as an independent oracle."""
    distinct = sorted({s for s in salaries if s is not None}, reverse=True)
    return distinct[1] if len(distinct) >= 2 else None


class TestSecondHighestSalary(unittest.TestCase):
    """Unit tests covering all three pandas solutions."""

    # Each case is (name, salaries, expected).
    KNOWN_CASES: list[tuple[str, list[int | None], int | None]] = [
        ("LeetCode example 1", [100, 200, 300], 200),
        ("LeetCode example 2", [100], None),
        ("empty table", [], None),
        ("duplicate top salary", [300, 300, 200], 200),
        ("all salaries equal", [100, 100, 100], None),
        ("exactly two distinct", [100, 200], 100),
        ("unsorted with duplicates", [200, 300, 100, 300], 200),
        ("negative salaries", [-5, -1, -10], -5),
        ("NaN among values", [None, 100, 200], 100),
        ("NaN and one value", [None, 100], None),
        ("only NaN", [None, None], None),
    ]

    def assert_result(self, result: pd.DataFrame, expected: int | None) -> None:
        """Check the shape (Q1) and the value, with None strictly None (Q2)."""
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(list(result.columns), ["SecondHighestSalary"])
        self.assertEqual(len(result), 1)

        value = result["SecondHighestSalary"].iloc[0]
        if expected is None:
            self.assertIsNone(value)
        else:
            self.assertEqual(value, expected)

    def test_known_cases(self) -> None:
        """Every solution returns the expected one-row frame on hand-picked cases."""
        for solution in SOLUTIONS:
            for name, salaries, expected in self.KNOWN_CASES:
                # subTest reports each failing (solution, case) pair separately.
                with self.subTest(solution=solution.__name__, case=name):
                    self.assert_result(solution(make_employee(salaries)), expected)

    def test_random_inputs_match_reference(self) -> None:
        """All solutions agree with the plain Python oracle on random inputs."""
        rng = random.Random(42)  # fixed seed keeps failures reproducible

        for _ in range(300):
            salaries: list[int | None] = [
                rng.choice([None, *range(-3, 6)]) for _ in range(rng.randint(0, 12))
            ]
            expected = reference(salaries)
            for solution in SOLUTIONS:
                with self.subTest(solution=solution.__name__, salaries=salaries):
                    self.assert_result(solution(make_employee(salaries)), expected)

    def test_does_not_mutate_input(self) -> None:
        """No solution may modify the caller's DataFrame (Q10)."""
        for solution in SOLUTIONS:
            employee = make_employee([200, 300, 100, 300])
            snapshot = employee.copy()
            with self.subTest(solution=solution.__name__):
                solution(employee)
                pd.testing.assert_frame_equal(employee, snapshot)


if __name__ == "__main__":
    unittest.main()