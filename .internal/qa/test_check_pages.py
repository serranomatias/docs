"""Regression tests for navigation, link and redirect validation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name("check-pages.py")


class PageChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.config = {
            "navigation": {"languages": [
                {"language": language, "tabs": [{"tab": "Guide", "groups": [
                    {"group": "Start here", "pages": [f"{language}/test"]}
                ]}]} for language in ("es", "en")
            ]},
            "redirects": [],
        }
        for language in ("es", "en"):
            self.page(f"{language}/test")

    def page(self, path, body=""):
        target = self.root / f"{path}.mdx"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('---\ntitle: Test\ndescription: Test page\n---\n' + body)

    def run_check(self, strict=False):
        (self.root / "docs.json").write_text(json.dumps(self.config))
        return subprocess.run(
            [sys.executable, str(CHECKER), f"--root={self.root}"]
            + (["--strict"] if strict else []),
            capture_output=True, text=True, check=False,
        )

    def test_nested_navigation_ignores_display_labels(self):
        result = self.run_check(strict=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("docs.json: 2", result.stdout)

    def test_navigation_entry_does_not_make_missing_link_valid(self):
        (self.root / "en/test.mdx").unlink()
        self.page("es/test", "[English](/en/test)")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("pero no existe el archivo", result.stdout)
        self.assertIn("enlace interno roto", result.stdout)

    def test_redirect_destination_must_exist(self):
        self.config["redirects"] = [{"source": "/old", "destination": "/en/missing"}]
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("destino de redirección inexistente", result.stdout)

    def test_parity_traverses_nested_groups(self):
        self.page("es/extra")
        self.config["navigation"]["languages"][0]["tabs"][0]["groups"][0]["pages"].append("es/extra")
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("paridad ES/EN", result.stdout)

    def test_orphan_fails_only_in_strict_mode(self):
        self.page("en/orphan")
        self.assertEqual(self.run_check().returncode, 0)
        result = self.run_check(strict=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("página huérfana", result.stdout)

    def test_duplicate_and_self_redirects_fail(self):
        self.config["redirects"] = [
            {"source": "/en/test", "destination": "/en/test"},
            {"source": "/en/test", "destination": "/es/test"},
        ]
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("redirección duplicada", result.stdout)
        self.assertIn("redirección a sí misma", result.stdout)


if __name__ == "__main__":
    unittest.main()
