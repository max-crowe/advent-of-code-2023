from io import StringIO
from unittest import TestCase

from .handler import NoDigitsInStringError, handle, handle_with_replacement, replace_named_digits


class HandlerTestCase(TestCase):
    def test_handles_expected_input(self):
        test_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
        expected = [12, 38, 15, 77]
        actual = [handle(line) for line in StringIO(test_input)]
        self.assertEqual(expected, actual)

    def test_raises_error_when_input_contains_no_digits(self):
        with self.assertRaises(NoDigitsInStringError):
            handle("foo")

    def test_handles_expected_input_with_replacement(self):
        test_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
        expected = [29, 83, 13, 24, 42, 14, 76]
        actual = [handle_with_replacement(line) for line in StringIO(test_input)]
        self.assertEqual(expected, actual)

    def test_handles_expected_input_with_replacement_2(self):
        test_input = """1ggkrvbpsl9ssix6one8zh
679one9nzsktvfseighteightwotjm
threefive7gfzptnxbvvlzlxbteightglseightworsq
twotwo8rzdbgeightthree
sevenztlzzn38nine3jtnqjsnine6
14qrvcspxmr4
783sixxkkhrpqjrt5ninesjflktt1
73five3
nrtwonetlmkldqrcjqrdn6gptzdclninethreenine
8sixxqfl
sndlpvjr3
hx5zzlqk1571three
zvl1
1twotnqcmfqrnr33rrhghsdqddpmbzd
nine1threevcninetwosix7m
six2onesix1xqjzczdrl3
15jkhgkfzseven26
fntvfkhfzsfour7onesevenfour
nineight
"""
        expected = [
            18,
            62,
            32,
            23,
            76,
            14,
            71,
            73,
            29,
            86,
            33,
            53,
            11,
            13,
            97,
            63,
            16,
            44,
            98,
        ]
        actual = [handle_with_replacement(line) for line in StringIO(test_input)]
        self.assertEqual(expected, actual)
