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
import types
import unittest
from unittest import mock

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


def literal_row(name, *, main=False, valid=True, locked=False, classification="merged-removable",
                registered=True):
    """A lane G WorktreeRow written as a literal (lead ruling R-56): the fields
    the gates read, and its `main`, `raw_path` and `registered` attributes."""
    raw = b"/w/" + name.encode() + (b"" if valid else b"\xff")
    row = project.WorktreeRow(path=project.json_path(raw)[0], branch=name, locked=locked,
                              classification=classification, path_valid_utf8=valid)
    row.raw_path, row.main, row.registered = raw, main, registered
    return row


def literal_plan(mode, target=None):
    """A Plan of mode for the literal rows, P being target in mode single."""
    plan = project.Plan({"root": Path("/w/main")}, types.SimpleNamespace(
        mode=mode, action=None if mode == "report" else "remove"))
    plan.target = target
    return plan


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

    # T040: the first gates, the plan document and the estimates.

    def test_clean_first_gates_in_order(self):
        # FR-020, data-model.md "Gate": gate_rows() on literal rows, with no
        # child and no filesystem call; the first failing gate is the reason.
        main = literal_row("main", main=True, valid=False, locked=True, classification="protected-default")
        rows = {
            "bytes": literal_row("bytes", valid=False, locked=True, classification="dirty"),
            "locked": literal_row("locked", locked=True, classification="dirty"),
            "dirty": literal_row("dirty", classification="dirty"),
            # Lead ruling R-53 P-16: a registration never read passes gate 3 and
            # is excluded at gate 5 by its class, never as registration-mismatch.
            "unread": literal_row("unread", classification="stale-worktree", registered=None),
            "unverified": literal_row("unverified", classification="inspection-error", registered=None),
            "p": literal_row("p"),
            "q": literal_row("q"),
        }
        expected = {"main": "main-worktree", "bytes": "unsupported-path-bytes", "locked": "locked-worktree",
                    "dirty": "dirty", "unread": "stale-worktree", "unverified": "inspection-error"}
        order = [main, rows["q"], rows["unverified"], rows["p"], rows["dirty"], rows["unread"],
                 rows["locked"], rows["bytes"]]

        def outcome(plan, gated=None):
            selected, excluded = project.gate_rows(gated or order, plan, None)
            return ([row["branch"] for row in selected], [(row["branch"], reason) for row, reason in excluded])

        def by_bytes(names):
            return sorted(names, key=lambda name: ({"main": main, **rows}[name]).raw_path)

        with mock.patch.object(project, "run_bounded", side_effect=AssertionError("a Git child ran")), \
                mock.patch.object(project, "fs_call", side_effect=AssertionError("a filesystem call ran")):
            for mode in ("all-safe", "report"):
                with self.subTest(mode=mode):
                    self.assertEqual(outcome(literal_plan(mode)),
                                     (["p", "q"], [(name, expected[name]) for name in by_bytes(expected)]))
            with self.subTest("not-requested only in mode single, for a row other than P"):
                single = {**expected, "q": "not-requested"}
                self.assertEqual(outcome(literal_plan("single", rows["p"])),
                                 (["p"], [(name, single[name]) for name in by_bytes(single)]))
                none = {**expected, "p": "not-requested", "q": "not-requested"}
                self.assertEqual(outcome(literal_plan("single")),
                                 ([], [(name, none[name]) for name in by_bytes(none)]), "no single P: none selected")
            # The stubs' slots in the order: gate 3 after gate 2 and before gate 4,
            # gate 7 after gate 6, gate 8 over the rows past gate 7, and gates 9
            # and 10 only for the rows gate 8 takes.
            mismatched = literal_row("mismatched", locked=True, classification="inspection-error", registered=False)
            hidden = literal_row("bytes-mismatched", valid=False, registered=False)
            unstarted = literal_row("r")
            gated = [main, hidden, mismatched, rows["p"], rows["q"], unstarted]
            seen = []

            def reflog(row, plan, run):
                if row is unstarted:
                    row.unprobed = True  # R-67 (a): a read past its budget still names a reason
                    return "reflog-unavailable"
                return "unstarted-branch" if row is rows["q"] else None

            def index(row, plan, run):
                seen.append(row["branch"])
                return "hidden-local-state" if row is rows["p"] else None

            with mock.patch.object(project, "registration_gate",
                                   side_effect=lambda row, plan, run: "registration-mismatch"
                                   if row.registered is False else None), \
                    mock.patch.object(project, "reflog_gate", side_effect=reflog), \
                    mock.patch.object(project, "index_gates", side_effect=index):
                self.assertEqual(outcome(literal_plan("all-safe"), gated), ([], sorted([
                    ("main", "main-worktree"), ("bytes-mismatched", "unsupported-path-bytes"),
                    ("mismatched", "registration-mismatch"), ("p", "hidden-local-state"),
                    ("q", "unstarted-branch"), ("r", "reflog-unavailable")],
                    key=lambda item: b"/w/" + item[0].encode() + (b"\xff" if item[0] == "bytes-mismatched" else b""))))
                self.assertEqual(seen, ["p"])
                seen.clear()
                self.assertEqual(outcome(literal_plan("single", unstarted), gated)[1][-2:],
                                 [("q", "not-requested"), ("r", "reflog-unavailable")])
                # Gate 8 takes the first candidate and defers the rest: the
                # deferred row gets no index gate.
                with mock.patch.object(project, "deferral_gate",
                                       side_effect=lambda candidates, plan: (candidates[:1], candidates[1:])), \
                        mock.patch.object(project, "reflog_gate", return_value=None):
                    seen.clear()
                    self.assertEqual(outcome(literal_plan("report"), [main, rows["p"], rows["q"]]),
                                     ([], [("main", "main-worktree"), ("p", "hidden-local-state"),
                                           ("q", "deferred-target-cap")]))
                    self.assertEqual(seen, ["p"])
        # Each stub passes every row, and the deferral stub takes every candidate.
        plan = literal_plan("all-safe")
        for row in (main, *rows.values()):
            self.assertEqual([gate(row, plan, None) for gate in (project.registration_gate, project.reflog_gate,
                                                                  project.index_gates)], [None] * 3)
        self.assertEqual(project.deferral_gate([rows["p"], rows["q"]], plan), ([rows["p"], rows["q"]], []))


if __name__ == "__main__":
    unittest.main()
