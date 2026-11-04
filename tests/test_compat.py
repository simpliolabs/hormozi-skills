"""Native compatibility metadata: marketplace paths, version, skills declaration, optional Codex role adapters."""
import json
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EFFORT = {"sub-market": "medium", "sub-offer": "high", "sub-value": "medium",
          "sub-pricing": "high", "sub-sales": "medium", "hormozi-adversary": "high"}


def load(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


class TestManifests(unittest.TestCase):
    def test_codex_marketplace_source_resolves_inside_marketplace_root(self):
        for entry in load(".agents/plugins/marketplace.json")["plugins"]:
            target = (REPO / entry["source"]["path"]).resolve()
            target.relative_to(REPO.resolve())  # ../../ pointed outside the root and the plugin was not found
            self.assertTrue((target / ".codex-plugin" / "plugin.json").exists())
            self.assertEqual(target, REPO.resolve())

    def test_one_version_everywhere(self):
        versions = {
            load(".codex-plugin/plugin.json")["version"],
            load(".claude-plugin/plugin.json")["version"],
            load(".claude-plugin/marketplace.json")["metadata"]["version"],
            load(".claude-plugin/marketplace.json")["plugins"][0]["version"],
        }
        self.assertEqual(versions, {"1.1.1"})

    def test_codex_manifest_declares_existing_skills_dir_and_keeps_identity(self):
        m = load(".codex-plugin/plugin.json")
        self.assertEqual(m["name"], "hormozi-skills")
        self.assertTrue((REPO / m["skills"]).is_dir())
        self.assertEqual(m["author"]["name"], "Alessandro Smedile")
        self.assertEqual(load(".claude-plugin/plugin.json")["name"], "hormozi-skills")
        self.assertEqual(load(".claude-plugin/plugin.json")["author"]["name"], "Alessandro Smedile")

    def test_shared_assets_the_skills_need_are_packaged_at_plugin_root(self):
        for rel in ("references/orchestration.md", "references/evidence-contract.md",
                    "references/commercial-feasibility.md", "scripts/check_outputs.py", "contracts/brief.schema.json"):
            self.assertTrue((REPO / rel).exists(), rel)


class TestCodexRoleAdapters(unittest.TestCase):
    def cfg(self, name):
        return tomllib.loads((REPO / ".codex" / "agents" / f"{name}.toml").read_text(encoding="utf-8"))

    def test_six_adapters_exist_and_nothing_else(self):
        have = {p.stem for p in (REPO / ".codex" / "agents").glob("*.toml")}
        self.assertEqual(have, set(EFFORT))

    def test_requested_effort_and_no_model_id(self):
        for name, effort in EFFORT.items():
            c = self.cfg(name)
            self.assertEqual(c["name"], name)
            self.assertEqual(c["model_reasoning_effort"], effort, name)
            self.assertNotIn("model", c, f"{name}: unsupported model IDs must be omitted")
            self.assertIn("cannot calculate hashes", c["developer_instructions"], name)

    def test_adversary_is_read_only_and_specialists_point_at_their_role_file(self):
        self.assertEqual(self.cfg("hormozi-adversary")["sandbox_mode"], "read-only")
        for name in EFFORT:
            if name.startswith("sub-"):
                self.assertIn(f"agents/{name}.md", self.cfg(name)["developer_instructions"])
                self.assertTrue((REPO / "agents" / f"{name}.md").exists())

    def test_config_enables_agents_with_three_threads(self):
        c = tomllib.loads((REPO / ".codex" / "config.toml").read_text(encoding="utf-8"))
        self.assertEqual(c["agents"], {"enabled": True, "max_concurrent_threads_per_session": 3})

    def test_claude_baseline_unchanged(self):
        for name in ("sub-market", "sub-offer", "sub-value", "sub-pricing", "sub-sales", "hormozi-orchestrator"):
            self.assertIn("model: sonnet", (REPO / "agents" / f"{name}.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
