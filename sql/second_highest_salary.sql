-- =============================================================================
-- SECOND HIGHEST SALARY (PostgreSQL)
-- https://leetcode.com/problems/second-highest-salary/
-- Difficulty: Medium
-- =============================================================================
--
-- PROBLEM
-- Table Employee(id INT PRIMARY KEY, salary INT).
-- Return the second highest DISTINCT salary in a column named
-- SecondHighestSalary. If there is no second highest salary, return NULL.
-- The result must ALWAYS be exactly one row, even when the answer is NULL.
--
-- Example 1: salaries 100, 200, 300  ->  200
-- Example 2: salaries 100            ->  NULL
--
-- Pattern: "Nth highest" selection with distinct values, plus the
-- "empty result must become a NULL row" requirement.
--
-- HOW TO RUN
--   psql -d <database> -f second_highest_salary.sql
-- The script creates TEMP objects only, runs the self-checking tests at the
-- bottom, and prints "all tests passed" or raises an exception on failure.
-- To submit on LeetCode, copy only the SELECT statement of one solution (the
-- text after "AS" in its CREATE TEMP VIEW), not the view wrapper.
--
-- THE TWO TRAPS
-- 1. Duplicates: salaries 300, 300, 200 have second highest 200, not 300.
-- 2. The null row: a query that finds nothing returns ZERO rows, but the
--    problem demands ONE row containing NULL. Each solution below gets there
--    a different way (scalar subquery, aggregate over zero rows).
--
-- ┌──────────────────────────────┬────────────────┬──────────────┐
-- │ Approach                     │ Time           │ Space        │
-- ├──────────────────────────────┼────────────────┼──────────────┤
-- │ 1. DISTINCT + LIMIT/OFFSET   │ O(n log n)     │ O(d)         │
-- │ 2. MAX of values below MAX   │ O(n)           │ O(1)         │
-- │ 3. DENSE_RANK window         │ O(n log n)     │ O(n)         │
-- └──────────────────────────────┴────────────────┴──────────────┘
-- n = number of rows, d = number of distinct salaries (d <= n).
--
-- COMPLEXITY ANALYSIS
-- Solution 1: DISTINCT removes duplicates (hash or sort) and ORDER BY sorts
--   the d distinct values: O(n + d log d), which is O(n log n) worst case.
--   With a b-tree index on salary the planner can read the index backward
--   and stop after the second distinct value, so it can be far cheaper in
--   practice. Check with EXPLAIN before claiming it.
-- Solution 2: two aggregate passes over the table, no sort: O(n) time and
--   O(1) extra space. With an index on salary, the planner can answer each
--   MAX with a single index lookup.
-- Solution 3: the window function sorts the rows to rank them: O(n log n)
--   time, O(n) space. It is the most general solution (any N, any group).
--
-- INTERVIEW QUESTIONS AND PITFALLS
--
-- Q1. Why is DISTINCT needed in Solution 1?
--     Without it, salaries 300, 300, 200 sort to 300, 300, 200 and
--     OFFSET 1 returns 300, which is the highest again, not the second.
--
-- Q2. Why does the query have an outer SELECT with no FROM?
--     If the inner query finds no row, it returns zero rows and the result
--     set is empty, not a row with NULL. A scalar subquery in a SELECT list
--     evaluates to NULL when it returns no row, and the outer SELECT
--     without FROM always returns exactly one row.
--
-- Q3. Why do Solutions 2 and 3 not need that wrapper?
--     An aggregate without GROUP BY always returns exactly one row. MAX over
--     zero rows is NULL, so the row exists and holds NULL.
--
-- Q4. Why does MAX(DISTINCT salary) combined with OFFSET fail?
--     MAX collapses the whole table into a single row, so OFFSET 1 skips
--     that only row and the result is always empty. Aggregates and
--     OFFSET solve the problem in different ways and cannot be mixed.
--
-- Q5. What is the off-by-one in OFFSET?
--     OFFSET counts rows to skip. The Nth highest needs OFFSET N - 1. The
--     second highest is OFFSET 1, the third highest is OFFSET 2.
--
-- Q6. RANK vs DENSE_RANK vs ROW_NUMBER: which is correct here and why?
--     With salaries 300, 300, 200: ROW_NUMBER gives 1, 2, 3, so rank 2 is
--     300 (wrong, a duplicate). RANK gives 1, 1, 3, so rank 2 does not
--     exist and the result would be NULL (wrong). DENSE_RANK gives 1, 1, 2,
--     so rank 2 is 200 (correct). Ties must not consume rank numbers.
--
-- Q7. What is the PostgreSQL-specific NULL ordering pitfall?
--     In PostgreSQL, NULL sorts as larger than every value, so ORDER BY
--     salary DESC puts NULL FIRST. If salary is nullable, Solution 1
--     without a filter skips the NULL row at OFFSET 1 and returns the
--     highest salary instead of the second. MySQL sorts NULL as smallest,
--     which hides the bug on LeetCode. Filter with WHERE salary IS NOT NULL
--     (or use NULLS LAST). Solutions 2 and 3 are safe: NULL < x is NULL, and
--     MAX ignores NULL.
--
-- Q8. Why is the alias quoted as "SecondHighestSalary"?
--     PostgreSQL folds unquoted identifiers to lowercase, so the column
--     would be named secondhighestsalary. Quoting preserves the exact
--     capitalization the problem expects.
--
-- Q9. Which approach do you present first in an interview?
--     Solution 2, because it has no ranking logic, no wrapper and gets
--     the NULL row for free. Then mention Solution 3 as the one that
--     generalizes, and ask whether salary can be NULL and whether ties
--     matter.
--
-- Q10. Follow-up: how do you get the Nth highest salary?
--      Solution 1 generalizes with OFFSET N - 1, which PostgreSQL accepts as
--      an expression inside a function parameter, but a negative offset
--      raises an error, so validate N >= 1. Solution 3 generalizes with
--      WHERE rnk = N. Solution 2 does not generalize, because it would
--      need N nested MAX subqueries.
--
-- Q11. Follow-up: the second highest salary PER DEPARTMENT?
--      Add PARTITION BY department to the window:
--      DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC).
--      Solutions 1 and 2 do not extend cleanly. This is the same pattern
--      as LeetCode 185, Department Top Three Salaries.
--
-- Q12. Why does the subquery in FROM have an alias in Solution 3?
--      PostgreSQL before version 16 rejects a FROM subquery without an
--      alias ("subquery in FROM must have an alias"). MySQL rejects it as
--      well. Always alias derived tables.
--
-- Q13. How would you make this fast on a table with 100 million rows?
--      Create a b-tree index on salary. Solution 2 can then run both MAX
--      calls as index lookups. Solution 1 can read the index backward and
--      stop early. Confirm both with EXPLAIN (ANALYZE).
-- =============================================================================


-- -----------------------------------------------------------------------------
-- SETUP (temp objects that shadow any real Employee table and are dropped
-- automatically when the session ends, so run this file in a fresh session)
-- -----------------------------------------------------------------------------
CREATE TEMP TABLE Employee (
    id     INT PRIMARY KEY,
    salary INT
);


-- -----------------------------------------------------------------------------
-- SOLUTION 1: DISTINCT + ORDER BY + LIMIT/OFFSET inside a scalar subquery
-- Distinct salaries sorted descending, skip the highest, take the next one.
-- The outer SELECT turns "no row" into a NULL row (Q2). The IS NOT NULL filter
-- protects against PostgreSQL sorting NULL first on DESC (Q7).
-- -----------------------------------------------------------------------------
CREATE TEMP VIEW solution_1_limit_offset AS
SELECT (
    SELECT DISTINCT salary
    FROM Employee
    WHERE salary IS NOT NULL
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
) AS "SecondHighestSalary";


-- -----------------------------------------------------------------------------
-- SOLUTION 2: MAX of the salaries strictly below the overall MAX
-- The second highest distinct salary is the largest value that is less than
-- the largest value. "Strictly less" removes duplicates of the top salary
-- automatically, so no DISTINCT is needed. MAX over zero rows returns NULL,
-- so the NULL row comes for free (Q3).
-- -----------------------------------------------------------------------------
CREATE TEMP VIEW solution_2_max_below_max AS
SELECT MAX(salary) AS "SecondHighestSalary"
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);


-- -----------------------------------------------------------------------------
-- SOLUTION 3: DENSE_RANK window function
-- DENSE_RANK gives tied salaries the same rank and does not skip numbers
-- (Q6). The outer MAX guarantees exactly one row, NULL when rank 2 does not
-- exist. Change "rnk = 2" to "rnk = N" for the Nth highest (Q10).
-- -----------------------------------------------------------------------------
CREATE TEMP VIEW solution_3_dense_rank AS
SELECT MAX(salary) AS "SecondHighestSalary"
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM Employee
    WHERE salary IS NOT NULL
) AS ranked
WHERE rnk = 2;


-- -----------------------------------------------------------------------------
-- TESTS (self-checking: raises an exception on the first failure)
-- Each scenario reloads Employee, then every solution must return exactly one
-- row whose value matches the expectation, NULL included.
-- -----------------------------------------------------------------------------
DO $$
DECLARE
    scenario  RECORD;
    solution  TEXT;
    actual    INT;
    row_count INT;
    checks    INT := 0;
BEGIN
    FOR scenario IN
        SELECT * FROM (VALUES
            ('LeetCode example 1',          ARRAY[100, 200, 300]::INT[],     200),
            ('LeetCode example 2',          ARRAY[100]::INT[],               NULL),
            ('empty table',                 ARRAY[]::INT[],                  NULL),
            ('duplicate top salary',        ARRAY[300, 300, 200]::INT[],     200),
            ('all salaries equal',          ARRAY[100, 100, 100]::INT[],     NULL),
            ('exactly two distinct',        ARRAY[100, 200]::INT[],          100),
            ('unsorted with duplicates',    ARRAY[200, 300, 100, 300]::INT[], 200),
            ('negative salaries',           ARRAY[-5, -1, -10]::INT[],       -5),
            ('NULL among values (Q7)',      ARRAY[NULL, 100, 200]::INT[],    100),
            ('NULL and one value',          ARRAY[NULL, 100]::INT[],         NULL),
            ('only NULLs',                  ARRAY[NULL, NULL]::INT[],        NULL)
        ) AS t(name, salaries, expected)
    LOOP
        DELETE FROM Employee;
        INSERT INTO Employee (id, salary)
        SELECT ord, val
        FROM unnest(scenario.salaries) WITH ORDINALITY AS u(val, ord);

        FOREACH solution IN ARRAY ARRAY[
            'solution_1_limit_offset',
            'solution_2_max_below_max',
            'solution_3_dense_rank'
        ]
        LOOP
            EXECUTE format('SELECT COUNT(*) FROM %I', solution) INTO row_count;
            IF row_count <> 1 THEN
                RAISE EXCEPTION 'FAIL [%] %: expected exactly 1 row, got %',
                    scenario.name, solution, row_count;
            END IF;

            EXECUTE format('SELECT "SecondHighestSalary" FROM %I', solution) INTO actual;
            IF actual IS DISTINCT FROM scenario.expected THEN
                RAISE EXCEPTION 'FAIL [%] %: expected %, got %',
                    scenario.name, solution, scenario.expected, actual;
            END IF;

            checks := checks + 1;
        END LOOP;
    END LOOP;

    RAISE NOTICE 'all tests passed (% checks)', checks;
END
$$;