import unittest

from fdct.confusables import get_alternatives
from fdct.generator import (
    CombinationLimitExceeded,
    build_plan,
    generate_combinations,
    iter_combinations,
)


class TestGenerator(unittest.TestCase):
    def test_correct_number_of_combinations(self):
        plan = build_plan("ab")
        expected = len(get_alternatives("a")) * len(get_alternatives("b"))
        self.assertEqual(plan.theoretical_count, expected)
        results = generate_combinations(plan)
        self.assertEqual(len(results), expected)

    def test_original_word_is_preserved(self):
        word = "hello"
        plan = build_plan(word)
        results = generate_combinations(plan)
        self.assertIn(word, results)

    def test_results_have_no_duplicates(self):
        plan = build_plan("cat")
        results = generate_combinations(plan)
        self.assertEqual(len(results), len(set(results)))

    def test_unicode_codepoints_differ_from_ascii(self):
        alternatives = get_alternatives("o")
        chars = [info.char for info in alternatives]
        # The original 'o' must be present, and at least one alternative
        # must be a genuinely different code point despite looking similar.
        self.assertIn("o", chars)
        self.assertTrue(any(ord(c) != ord("o") for c in chars))

    def test_combination_limit_protection(self):
        plan = build_plan("hello")
        with self.assertRaises(CombinationLimitExceeded):
            generate_combinations(plan, max_combinations=1)

    def test_force_bypasses_limit(self):
        plan = build_plan("ab")
        results = generate_combinations(plan, max_combinations=1, force=True)
        self.assertEqual(len(results), plan.theoretical_count)

    def test_iter_combinations_matches_generate(self):
        plan = build_plan("ab")
        self.assertEqual(sorted(iter_combinations(plan)), sorted(generate_combinations(plan)))


if __name__ == "__main__":
    unittest.main()
