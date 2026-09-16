"""Offline M0 checks for the synthetic procurement workflow skeleton."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class ProcurementFlowSkeletonTests(unittest.TestCase):
    def test_domain_covers_all_synthetic_workflow_records(self) -> None:
        source = (ROOT / "src" / "domain.ts").read_text(encoding="utf-8")

        for record in (
            "purchaseRequest",
            "supplierQuote",
            "approval",
            "delivery",
            "payment",
        ):
            self.assertIn(record, source)
        self.assertIn("Request-Aster", source)
        self.assertNotIn("http://", source)
        self.assertNotIn("https://", source)

    def test_project_charter_and_plan_are_present(self) -> None:
        specification = (ROOT / "SPEC.md").read_text(encoding="utf-8")
        plan = (ROOT / "PLANS.md").read_text(encoding="utf-8")

        for heading in ("## Problem", "## Target user", "## MVP scope", "## Explicit non-goals"):
            self.assertIn(heading, specification)
        for section in ("## Milestones", "## Progress log", "## Decision log"):
            self.assertIn(section, plan)
        self.assertIn("[x] **M0 setup**", plan)


if __name__ == "__main__":
    unittest.main()
