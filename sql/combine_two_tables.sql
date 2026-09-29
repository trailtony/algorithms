-- combine_two_tables.sql
-- LeetCode 175: Combine Two Tables
-- Goal: return firstName, lastName, city, state for every person,
-- even if that person has no row in Address.

SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM Person p
-- LEFT JOIN keeps every row from Person (the left/base table) regardless
-- of whether a match exists in Address. An INNER JOIN would silently
-- exclude any person with no address row, which breaks the problem spec.
LEFT JOIN Address a
    ON p.personID = a.personID;
-- Rows with no matching Address get NULL for city and state,
-- exactly mirroring SQL's own LEFT JOIN semantics.