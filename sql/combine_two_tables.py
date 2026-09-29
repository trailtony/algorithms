# combine_two_tables.py
# LeetCode 175: Combine Two Tables (pandas version)
# Same intent as the SQL solution: keep every person, attach address
# data where it exists, NaN where it doesn't.

import pandas as pd


def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    """Left-join Person to Address on personID, keeping unmatched persons."""
    # how="left" makes Person the base table — every row survives.
    # pandas' default merge is how="inner", which would drop any person
    # without a matching address row, so this must be explicit.
    result = person.merge(address, on="personID", how="left")

    # merge() brings along every column from both frames (including
    # personID twice, once per source unless renamed); select only the
    # columns the problem actually asks for.
    return result[["firstName", "lastName", "city", "state"]]