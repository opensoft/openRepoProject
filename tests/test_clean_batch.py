"""The plan of `project clean --all-safe` and of a named removal (feature 004,
the US1 plan lane: T036 to T040, and the tests T052 adds).

Sources: specs/004-project-clean-all-safe/contracts/project-clean.md
("Argument checks", "Order of a run", "Streams", "Human output", "Plan
envelope" and "Codes"), data-model.md ("Plan" and "Gate"), research.md R4 and
R12, and design.md D18 of openspec/changes/add-project-clean-all-safe/. Expected
human text comes from clean_support's fixtures (rule 8); key lists and parity
values are literals written here (rule 11). Every repository is a disposable
fixture under the test's temporary directory (rule 4); the eligible ones are
made by merged_worktree(), a commit of their own, so that US2's gates keep them
eligible (lead ruling R-56).
"""
import os
from pathlib import Path
import unittest

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# A well-formed --expect-plan value: 64 lowercase hexadecimal characters.
DIGEST = "0" * 64


def argv_words(record):
    """A counted child's argument vector without its leading -c pins."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


class BatchTests(clean_support.CleanCase):

    def counting(self, env=None):
        """The counting wrapper first on PATH (in front of the real git): returns
        the environment to run with and the log, emptied."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir, env), log

    def run_counted(self, *args, cwd=None, env=None):
        """`project ARGS...` under the counting wrapper: the run and its children."""
        env, log = self.counting(env)
        result = self.run_cli(*args, cwd=cwd, env=env)
        return result, clean_support.child_log(log)

    # T039: "Invalid argument combinations".

    def test_clean_invalid_argument_combinations(self):
        root = self.repo()
        tree = self.base / "w"
        cases = [
            (("--all-safe", "--action", "remove"), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--branch", "b"), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--worktree", tree), TEXT["invalid_arguments_all_safe"]),
            (("--all-safe", "--apply", "--action", "remove", "--worktree", tree),
             TEXT["invalid_arguments_all_safe"]),
            (("--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--all-safe", "--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--apply", "--expect-plan", DIGEST), TEXT["invalid_arguments_expect_plan"]),
            (("--apply", "--action", "remove", "--worktree", tree, "--expect-plan", DIGEST),
             TEXT["invalid_arguments_expect_plan"]),
            (("--all-safe", "--apply", "--expect-plan", "abc"), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "a" * 63), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "a" * 65), TEXT["invalid_arguments_expect_plan_value"]),
            (("--all-safe", "--apply", "--expect-plan", "A" * 64), TEXT["invalid_arguments_expect_plan_value"]),
            # The baseline's messages, now coded `invalid-arguments`.
            (("--apply",), "--apply requires --action push|remove|delete-branch"),
            (("--apply", "--action", "push"), "Push cleanup requires --branch BRANCH"),
            (("--apply", "--action", "remove"), "Worktree cleanup requires --worktree PATH"),
            (("--apply", "--action", "delete-branch"), "Branch cleanup requires --branch BRANCH"),
        ]
        json_kept = "--json cannot be combined with --apply; use JSON for the read-only plan."
        for extra, message in cases:
            # Under --json, push and delete-branch meet the kept --apply --json row first (below).
            for as_json in (False,) if "push" in extra or "delete-branch" in extra else (False, True):
                with self.subTest(arguments=[os.fspath(arg) for arg in extra], json=as_json):
                    words = (*extra, "--json") if as_json else extra
                    result, records = self.run_counted("clean", root, *words)
                    self.assert_status(result, 2)
                    self.assertEqual(records, [], "no child ran, not even git --version")
                    if as_json:
                        document = self.load_json(result)
                        self.assertEqual((document["code"], document["error"], document["refusals"]),
                                         ("invalid-arguments", message,
                                          [{"code": "invalid-arguments", "message": message}]))
                        self.assertEqual(result.stderr, "")
                    else:
                        self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {message}\n"))
        # --apply --json stays refused for push and delete-branch (OQ-10), with
        # the baseline's message, now coded.
        for action in ("push", "delete-branch"):
            with self.subTest(action=action, json=True):
                result, records = self.run_counted("clean", root, "--apply", "--action", action,
                                                   "--branch", "b", "--json")
                self.assert_status(result, 2)
                self.assertEqual(records, [])
                document = self.load_json(result)
                self.assertEqual((document["code"], document["error"]), ("invalid-arguments", json_kept))
        # An argument-parser usage error prints the parser's message, exits 2
        # and prints no JSON document.
        for words in (("--all-safe", "--apply", "--expect-plan"), ("--action", "bogus"), ("--no-such-flag",)):
            with self.subTest(usage=words):
                result, records = self.run_counted("clean", root, *words, "--json")
                self.assert_status(result, 2)
                self.assertEqual((result.stdout, records), ("", []))
                self.assertIn("usage: project", result.stderr)

    def test_clean_invalid_argument_combinations_unrefused_flags(self):
        # Plan review M9: flags no row of the table refuses keep the baseline's
        # handling.
        root = self.repo()
        self.bare_remote()
        merged = self.merged_worktree("001-merged")
        dirty = self.merged_worktree("002-dirty")
        (dirty / "uncommitted").write_text("preserve")
        before = self.git(root, "worktree", "list", "--porcelain")
        # Without --apply, --yes, --action, --branch and --worktree are ignored:
        # the run is a report (or, with --all-safe, a preview), exit 0.
        plain = self.load_json(self.run_cli("clean", root, "--json"))
        for extra in (("--yes",), ("--action", "remove"), ("--action", "push"), ("--branch", "002-dirty"),
                      ("--worktree", merged), ("--action", "remove", "--worktree", merged, "--yes")):
            with self.subTest(ignored=[os.fspath(arg) for arg in extra]):
                result = self.run_cli("clean", root, *extra, "--json")
                self.assert_status(result, 0)
                document = self.load_json(result)
                self.assertEqual(document["target_branch"], "main")
                self.assertEqual([(row["path"], row["classification"]) for row in document["worktrees"]],
                                 [(row["path"], row["classification"]) for row in plain["worktrees"]])
        with self.subTest(ignored=["--all-safe", "--yes"]):
            self.assert_status(self.run_cli("clean", root, "--all-safe", "--yes"), 0)
        # An unused --branch beside --apply --action remove, or --worktree beside
        # --apply --action push, is ignored: the run ends as it does without it.
        pairs = [
            (("--apply", "--action", "remove", "--worktree", dirty, "--yes"), ("--branch", "001-merged")),
            (("--apply", "--action", "push", "--branch", "002-dirty", "--yes"), ("--worktree", merged)),
        ]
        for words, unused in pairs:
            with self.subTest(unused=[os.fspath(arg) for arg in unused]):
                without = self.run_cli("clean", root, *words)
                given = self.run_cli("clean", root, *words, *unused)
                self.assert_status(without, 2)
                self.assertEqual((given.returncode, given.stdout, given.stderr),
                                 (without.returncode, without.stdout, without.stderr))
        self.assertEqual(self.git(root, "worktree", "list", "--porcelain"), before)
        self.assertTrue((dirty / "uncommitted").is_file())


if __name__ == "__main__":
    unittest.main()
