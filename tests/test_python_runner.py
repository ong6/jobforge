#!/usr/bin/env python3
"""The coding harness: python_runner.py and the run-solution.sh dispatcher.

Every test writes a throwaway solution + cases file and checks that exactly one JSON object comes
back on stdout with the right exit code, whatever the candidate code does.
"""

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "harness" / "python_runner.py"
DISPATCH = ROOT / "scripts" / "run-solution.sh"
CASES = {"function": "f", "cases": [{"args": [2], "expected": 4}]}


class Harness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        # A space in the directory name keeps the shell quoting honest.
        self.dir = pathlib.Path(self.tmp.name) / "work dir"
        self.dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, solution: str, cases=CASES):
        sol = self.dir / "sol.py"
        sol.write_text(solution, encoding="utf-8")
        cas = self.dir / "cases.json"
        cas.write_text(json.dumps(cases), encoding="utf-8")
        return str(sol), str(cas)

    def run_runner(self, solution: str, cases=CASES, timeout_s="1"):
        sol, cas = self.write(solution, cases)
        env = dict(os.environ, JOBFORGE_TIMEOUT_S=timeout_s)
        p = subprocess.run([sys.executable, str(RUNNER), sol, cas], capture_output=True, text=True,
                           env=env, timeout=20)
        return p.returncode, json.loads(p.stdout)

    def run_dispatch(self, *argv, timeout_s="1"):
        env = dict(os.environ, JOBFORGE_TIMEOUT_S=timeout_s)
        p = subprocess.run(["bash", str(DISPATCH), *argv], capture_output=True, text=True,
                           env=env, timeout=20)
        return p.returncode, p.stdout

    def test_pass(self):
        rc, out = self.run_runner("def f(x):\n    return x * 2\n")
        self.assertEqual((rc, out["passed"], out["total"], out["harness_error"]), (0, 1, 1, None))

    def test_wrong_answer(self):
        rc, out = self.run_runner("def f(x):\n    return x\n")
        self.assertEqual((rc, out["passed"]), (1, 0))
        self.assertEqual(out["cases"][0]["got"], "2")

    def test_exception_is_reported_per_case(self):
        rc, out = self.run_runner("def f(x):\n    raise ValueError('boom')\n")
        self.assertEqual(rc, 1)
        self.assertEqual(out["cases"][0]["error"], "ValueError: boom")

    def test_candidate_prints_do_not_corrupt_json(self):
        rc, out = self.run_runner("import sys\ndef f(x):\n    print('debug {')\n    sys.stderr.write('e\\n')\n    return 4\n")
        self.assertEqual((rc, out["passed"]), (0, 1))

    def test_timeout_survives_a_catch_all_except(self):
        """A `while True: try/except Exception: pass` loop used to swallow the timeout and hang."""
        rc, out = self.run_runner(
            "import time\ndef f(x):\n    while True:\n        try:\n            time.sleep(0.05)\n"
            "        except Exception:\n            pass\n")
        self.assertEqual(rc, 1)
        self.assertTrue(out["cases"][0]["timed_out"])

    def test_import_hang_is_bounded(self):
        rc, out = self.run_runner("while True:\n    pass\n")
        self.assertEqual(rc, 1)
        self.assertIn("hung at import", out["harness_error"])

    def test_sys_exit_in_solution(self):
        rc, out = self.run_runner("import sys\ndef f(x):\n    sys.exit(3)\n")
        self.assertEqual(rc, 1)
        self.assertIn("sys.exit(3)", out["cases"][0]["error"])

    def test_missing_function(self):
        rc, out = self.run_runner("def g(x):\n    return x\n")
        self.assertEqual(rc, 1)
        self.assertIn("not found", out["harness_error"])

    def test_bad_cases_file(self):
        rc, out = self.run_runner("def f(x):\n    return x\n", cases={"cases": []})
        self.assertEqual(rc, 2)
        self.assertIn("bad cases file", out["harness_error"])

    def test_unordered_and_tuple_normalisation(self):
        cases = {"function": "f", "unordered": True, "cases": [{"args": [], "expected": [[1, 2], [3, 4]]}]}
        rc, out = self.run_runner("def f():\n    return [(3, 4), (1, 2)]\n", cases=cases)
        self.assertEqual((rc, out["passed"]), (0, 1))

    def test_dispatch_pass_and_usage(self):
        sol, cas = self.write("def f(x):\n    return x * 2\n")
        rc, stdout = self.run_dispatch("python", sol, cas)
        self.assertEqual((rc, json.loads(stdout)["passed"]), (0, 1))
        rc, stdout = self.run_dispatch("python")
        self.assertEqual(rc, 2)
        self.assertIn("usage", json.loads(stdout)["harness_error"])
        rc, stdout = self.run_dispatch("rust", sol, cas)
        self.assertEqual(rc, 3)

    def test_dispatch_escapes_quotes_in_paths(self):
        rc, stdout = self.run_dispatch("python", str(self.dir / 'no"such\\file.py'), "x")
        self.assertEqual(rc, 2)
        self.assertIn('no"such\\file.py', json.loads(stdout)["harness_error"])

    def test_dispatch_reports_adapter_crash(self):
        """A hard crash (segfault) used to produce empty stdout and exit 139; now still one JSON line."""
        sol, cas = self.write("import ctypes\ndef f(x):\n    ctypes.string_at(0)\n")
        rc, stdout = self.run_dispatch("python", sol, cas)
        self.assertEqual(rc, 1)
        self.assertIn("no output", json.loads(stdout)["harness_error"])


if __name__ == "__main__":
    unittest.main()
