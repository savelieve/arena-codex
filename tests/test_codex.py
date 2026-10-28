"""Observable CLI checks for the Codex adaptation."""
import json
import unittest

from test_bracket import cli


class CodexScheduling(unittest.TestCase):
    def test_quick_default_schedule(self):
        result = cli('plan', '--quick', '--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        self.assertEqual((plan['agents'], plan['rounds'], plan['calls'], plan['waves']),
                         (16, 4, 91, 37))

    def test_invalid_wave_is_actionable_error(self):
        for wave in ('0', '-1'):
            result = cli('plan', '--quick', '--wave', wave)
            self.assertEqual(result.returncode, 2)
            self.assertIn('--wave must be at least 1', result.stderr)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
