import unittest

from fdct.validator import InvalidInputError, validate_word


class TestValidator(unittest.TestCase):
    def test_valid_lowercase_word(self):
        self.assertEqual(validate_word("hello"), "hello")
        self.assertEqual(validate_word("security"), "security")
        self.assertEqual(validate_word("administrator"), "administrator")

    def test_rejects_uppercase(self):
        with self.assertRaises(InvalidInputError):
            validate_word("Hello")

    def test_rejects_numbers(self):
        with self.assertRaises(InvalidInputError):
            validate_word("hello123")
        with self.assertRaises(InvalidInputError):
            validate_word("h3llo")

    def test_rejects_spaces(self):
        with self.assertRaises(InvalidInputError):
            validate_word("hello world")

    def test_rejects_punctuation(self):
        with self.assertRaises(InvalidInputError):
            validate_word("hello!")
        with self.assertRaises(InvalidInputError):
            validate_word("hello-world")

    def test_rejects_persian_arabic(self):
        with self.assertRaises(InvalidInputError):
            validate_word("سلام")

    def test_rejects_other_unicode(self):
        with self.assertRaises(InvalidInputError):
            validate_word("hellо")  # contains a Cyrillic 'о'

    def test_rejects_empty_input(self):
        with self.assertRaises(InvalidInputError):
            validate_word("")


if __name__ == "__main__":
    unittest.main()
