import unittest

from prototypes.scenarios.article01 import run as run_01
from prototypes.scenarios.article02 import run as run_02
from prototypes.scenarios.article03 import run as run_03
from prototypes.scenarios.article04 import run as run_04
from prototypes.scenarios.article05 import validate_steps


class EarlyScenarioTests(unittest.TestCase):
    def test_01_reports_retrieval_separately_from_generation(self):
        result = run_01(seed=17)
        self.assertEqual(result["evidence_type"], "synthetic")
        self.assertEqual(result["corpus_version"], "projects_v2")
        self.assertIn("retrieval", result)
        self.assertNotIn("llm_accuracy", result)

    def test_02_checks_exact_binary_dot_products(self):
        result = run_02(seed=17)
        self.assertEqual(result["evidence_type"], "computed")
        self.assertEqual(result["vectors_checked"], 1000)
        self.assertEqual(result["status"], "PASS")

    def test_03_keeps_total_work_budget_equal(self):
        result = run_03(seed=17)
        budgets = {row["workers"]: row["work_budget"] for row in result["results"]}
        self.assertEqual(set(budgets), {1, 3, 15})
        self.assertEqual(len(set(budgets.values())), 1)

    def test_04_generated_repository_contains_search_target(self):
        result = run_04(seed=17, file_count=200)
        self.assertEqual(result["file_count"], 200)
        self.assertEqual(result["lookup"]["found"], True)
        self.assertGreater(result["lookup"]["files_examined"], 0)
        self.assertIn("indexed_lookup_ms", result["lookup"])

    def test_05_training_steps_are_validated(self):
        self.assertEqual(validate_steps(3), 3)
        with self.assertRaisesRegex(ValueError, "positive"):
            validate_steps(0)


if __name__ == "__main__":
    unittest.main()
