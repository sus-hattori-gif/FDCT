import tempfile
import unittest
from pathlib import Path

from fdct.generator import build_plan, generate_combinations
from fdct.output import format_results_for_terminal, save_results


class TestOutput(unittest.TestCase):
    def setUp(self):
        self.word = "hi"
        plan = build_plan(self.word)
        self.results = generate_combinations(plan)

    def test_terminal_format_contains_all_results(self):
        text = format_results_for_terminal(self.word, self.results)
        self.assertIn(self.word, text)
        for combo in self.results:
            self.assertIn(combo, text)

    def test_utf8_file_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.txt"
            written_path = save_results(self.word, self.results, str(path))
            self.assertTrue(written_path.exists())
            content = written_path.read_text(encoding="utf-8")
            for combo in self.results:
                self.assertIn(combo, content)

    def test_default_filename_used(self):
        from fdct.output import DEFAULT_FILENAME

        self.assertEqual(DEFAULT_FILENAME, "FDCT_results.txt")


if __name__ == "__main__":
    unittest.main()
