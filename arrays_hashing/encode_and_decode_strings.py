"""Encode and Decode Strings (LeetCode 271): length-prefix encoding with loop concatenation vs join and str.index, with complexity analysis, interview notes and tests.

Pattern: Arrays & Hashing (string design, length-prefix framing).

PROBLEM
-------
Design encode(strs) -> str and decode(s) -> list[str] so that
decode(encode(strs)) == strs for ANY list of strings. The strings may
contain any character, including digits, delimiters and the empty string.
The functions must be stateless: decode cannot read anything saved by
encode except the encoded string itself.

THE IDEA
--------
Write each string as "<length>?<payload>". The decoder starts at the
beginning of a length prefix, reads digits up to the first "?", converts
them to an integer, then jumps forward exactly that many characters. The
payload is never inspected, so a "?" or digits inside a payload cannot be
confused with framing. The delimiter only needs to be a non-digit.

COMPLEXITY ANALYSIS
-------------------
Let N = total number of characters across all strings and m = number of
strings.

Solution 1, loop concatenation and manual scan:
    encode time:  O(N + m) in the best case. Repeated "+=" on a str is not
    guaranteed to be linear: CPython sometimes resizes in
    place, but the language does not promise it, and the
    worst case is O(N^2) because each concatenation may copy
    the whole accumulated string.
    decode time:  O(N + m). Each character is visited once, either while
    scanning a length prefix or while being sliced into a
    payload.
    Space:        O(N + m) for the encoded string and the decoded list.

Solution 2, join and str.index:
    encode time:  O(N + m). join computes the final size once and copies
    each piece once, so linear on every implementation.
    decode time:  O(N + m). str.index scans for "?" at C speed and each
    payload is sliced once.
    Space:        O(N + m).

Alternatives worth naming (not implemented here):
    Escape scheme: pick a delimiter, replace it inside payloads with an
    escape sequence, and escape the escape character too. O(N) time but
    the decoder must track escape state, which is easy to get wrong.
    Fixed-width header: prefix every string with its length padded to a
    fixed number of digits (for example 4). Simple to parse but caps the
    string length at 9999 and wastes space on short strings.

INTERVIEW QUESTIONS AND PITFALLS
--------------------------------
Q1. Why not join with a delimiter and split on it in decode?
    Any delimiter you choose can appear inside a payload, and then split
    returns the wrong pieces. For example, joining ["a,b", "c"] with "," and
    splitting gives three strings instead of two. The delimiter must be
    unrecoverable from the content, and the length prefix achieves that.

Q2. Why does a "?" or a digit inside a payload not break the length prefix?
    The decoder always stands at the start of a prefix when it searches
    for "?", and after reading the length it skips the payload without
    looking at it. Content is only ever copied, never parsed.

Q3. Can the delimiter be a digit?
    No. The length is the run of digits before the delimiter, so a digit
    delimiter would merge into the number. Any non-digit works. The choice
    of "?" is arbitrary.

Q4. How do you distinguish an empty list from a list with one empty string?
    [] encodes to "" and [""] encodes to "0?". The decoder returns [] for
    "" because the loop never runs, and [""] for "0?" because it reads
    length 0 and appends an empty slice. The two cases must be tested
    separately, and a naive delimiter scheme often conflates them.

Q5. Why prefer join over += in encode?
    Repeated concatenation can degrade to O(N^2) on implementations that
    do not resize strings in place. join builds the result in one pass on
    every implementation. This is the difference interviewers look for.

Q6. Why is str.index better than a manual while loop for finding "?"?
    It is shorter, runs at C speed, and raises ValueError when "?" is
    missing. The manual loop runs off the end and raises IndexError, which
    hides the real cause (malformed input) behind an out-of-range message.

Q7. What does "stateless" mean here and why does it matter?
    encode and decode may run on different machines or in different
    processes. Storing the original list in a class attribute or a global
    "to look up later" is cheating and fails the problem's contract. The
    encoded string must carry all the information.

Q8. What changes if the strings travel over a network as UTF-8 bytes?
    len(s) counts characters, not bytes. If the receiver slices the raw
    byte stream, any non-ASCII character makes the declared length wrong.
    Encode to bytes first and prefix with the byte length, or decode the
    bytes back to str before slicing.

Q9. What is the downside of the fixed-width header alternative?
    It limits the maximum string length (4 digits means 9999) and pads
    short strings, so it wastes space. Variable-width prefixes with a
    delimiter have no length cap.

Q10. How does decode behave on malformed input?
It trusts the input. A missing "?" raises ValueError in Solution 2 
(IndexError in Solution 1). Non-numeric text before "?" raises
ValueError from int(). A length that exceeds the remaining text is
not detected: the slice silently returns the shorter tail. A
production decoder would validate j + 1 + length <= len(s).

Q11. Follow-up: how would you do this for a stream you cannot hold in memory?
Length-prefix framing is exactly what network protocols use (for
example, HTTP/2 frames and Redis RESP bulk strings). The reader
reads the prefix, then reads exactly that many bytes, without ever
buffering the whole message.
"""

import random
import unittest


class SolutionConcat:
    """Length-prefix codec using loop concatenation and a manual delimiter scan."""

    def encode(self, strs: list[str]) -> str:
        """Encode a list of strings as length-prefixed chunks using += concatenation."""
        encoded = ""
        for s in strs:
            encoded += f"{len(s)}?{s}"
        return encoded

    def decode(self, s: str) -> list[str]:
        """Decode a length-prefixed string by scanning for the delimiter by hand."""
        decoded: list[str] = []
        i = 0

        while i < len(s):
            j = i
            while s[j] != "?":
                j += 1
            length = int(s[i:j])
            decoded.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length

        return decoded


class Solution:
    """Length-prefix codec using join and str.index, the preferred interview answer."""

    def encode(self, strs: list[str]) -> str:
        """Encode a list of strings as length-prefixed chunks using join."""
        return "".join(f"{len(s)}?{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        """Decode a length-prefixed string back into the original list."""
        decoded: list[str] = []
        i = 0

        while i < len(s):
            # i always sits at the start of a length prefix, so the first "?"
            # found from here is the delimiter, never one inside a payload.
            j = s.index("?", i)
            length = int(s[i:j])
            decoded.append(s[j + 1 : j + 1 + length])
            i = j + 1 + length

        return decoded


# ---------------------------------------------------------------------------
# Tests (run with: uv run python -m unittest -v encode_and_decode_strings)
# ---------------------------------------------------------------------------

CODECS: list[type[SolutionConcat] | type[Solution]] = [SolutionConcat, Solution]


class TestEncodeDecode(unittest.TestCase):
    """Unit tests covering round trips, edge cases and malformed input."""

    ROUND_TRIP_CASES: list[list[str]] = [
        ["neet", "code", "love", "you"],  # LeetCode example 1
        ["we", "say", ":", "yes"],  # LeetCode example 2
        [],  # empty list (Q4)
        [""],  # one empty string (Q4)
        ["", ""],  # several empty strings
        ["a"],  # single character
        ["?"],  # payload is the delimiter
        ["3?abc"],  # payload that looks like an encoded chunk
        ["1?", "2?a", "0?"],  # many delimiter-like payloads
        ["123", "4567", "0"],  # numeric payloads
        ["a,b", "c"],  # the string that breaks join/split (Q1)
        ["line1\nline2", "tab\there"],  # whitespace characters
        ["日本語", "é", "😀"],  # non-ASCII characters
        ["x" * 1000, "y" * 12, ""],  # multi-digit length prefix
    ]

    def test_round_trip_known_cases(self) -> None:
        """decode(encode(strs)) returns the original list for every known case."""
        for codec_cls in CODECS:
            codec = codec_cls()
            for strs in self.ROUND_TRIP_CASES:
                with self.subTest(codec=codec_cls.__name__, strs=strs):
                    self.assertEqual(codec.decode(codec.encode(strs)), strs)

    def test_empty_list_and_single_empty_string_are_distinct(self) -> None:
        """[] and [""] must encode to different strings (Q4)."""
        for codec_cls in CODECS:
            codec = codec_cls()
            with self.subTest(codec=codec_cls.__name__):
                self.assertEqual(codec.encode([]), "")
                self.assertEqual(codec.encode([""]), "0?")

    def test_both_codecs_produce_identical_encoding(self) -> None:
        """The two implementations are wire-compatible in both directions."""
        concat, joined = SolutionConcat(), Solution()
        for strs in self.ROUND_TRIP_CASES:
            with self.subTest(strs=strs):
                encoded = concat.encode(strs)
                self.assertEqual(encoded, joined.encode(strs))
                self.assertEqual(joined.decode(encoded), strs)
                self.assertEqual(concat.decode(joined.encode(strs)), strs)

    def test_random_round_trip(self) -> None:
        """Random lists over a hostile alphabet survive a round trip."""
        rng = random.Random(42)  # fixed seed keeps failures reproducible
        alphabet = "ab12?: \n"  # digits and the delimiter on purpose

        for _ in range(500):
            strs = [
                "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
                for _ in range(rng.randint(0, 6))
            ]
            for codec_cls in CODECS:
                codec = codec_cls()
                with self.subTest(codec=codec_cls.__name__, strs=strs):
                    self.assertEqual(codec.decode(codec.encode(strs)), strs)

    def test_malformed_input_error_types(self) -> None:
        """A missing delimiter raises ValueError (index) or IndexError (manual scan), per Q6."""
        with self.assertRaises(ValueError):
            Solution().decode("5abc")
        with self.assertRaises(IndexError):
            SolutionConcat().decode("5abc")


if __name__ == "__main__":
    unittest.main()
