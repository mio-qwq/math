"""Cross-encoding feasibility checks and parameter/boundary regressions."""
import itertools
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from corridor import solve as horizon_solve
from rob import Program, solve as optimize
from checker import replay


class CorridorTests(unittest.TestCase):
    def test_all_small_graph_resource_horizons(self):
        cases = 0
        for n in range(5):
            pairs = [(i, j) for j in range(n) for i in range(j)]
            for mask in range(1 << len(pairs)):
                edges = [e for k, e in enumerate(pairs) if mask >> k & 1]
                for b, w in itertools.product(range(1, n + 2), repeat=2):
                    optimum = optimize(Program(n, tuple(edges)), b, w)["cycles"]
                    for h in range(n + 2):
                        out = horizon_solve(n, edges, b, w, h)
                        self.assertEqual(out["feasible"], optimum <= h, (n, edges, b, w, h))
                        if out["feasible"]:
                            replay(n, edges, b, w, out["schedule"])
                            self.assertLessEqual(len(out["schedule"]), h)
                        cases += 1
        self.assertEqual(cases, 10326)

    def test_large_width_small_parameter(self):
        # The full completed-set solver need not be invoked on this large width.
        for edges, expected in [([], True), ([(0, 49)], True), ([(0, 1)], False)]:
            out = horizon_solve(300, edges, 51, 50, 6)
            self.assertEqual(out["feasible"], expected)
            self.assertEqual(out["states_per_layer_bound"], 2)
            self.assertLessEqual(max(out["candidate_sizes"]), 2)
            if expected:
                replay(300, edges, 51, 50, out["schedule"])
                self.assertEqual(len(out["schedule"]), 6)

    def test_dummy_padding_is_not_equivalent(self):
        edges = [(0, 1)]
        yes = horizon_solve(5, edges, 4, 3, 2)
        no = horizon_solve(6, edges, 4, 3, 2)
        self.assertTrue(yes["feasible"])
        self.assertEqual(yes["idle_slot_budget"], 1)
        self.assertFalse(no["feasible"])
        replay(5, edges, 4, 3, yes["schedule"])

    def test_large_horizon_shortcuts_and_forward_validation(self):
        out = horizon_solve(7, [(i, i + 1) for i in range(6)], 2, 50, 10**9)
        self.assertEqual(out["schedule"], [[i] for i in range(7)])
        self.assertEqual(horizon_solve(0, [], 1, 1, 10**9)["schedule"], [])
        for args in [(-1, [], 1, 1, 0), (1, [], 0, 1, 1),
                     (1, [], 1, 0, 1), (1, [], 1, 1, -1),
                     (2, [(1, 0)], 1, 1, 9), (0, [(0, 1)], 1, 1, 0)]:
            with self.assertRaises(ValueError):
                horizon_solve(*args)


if __name__ == "__main__":
    unittest.main()
