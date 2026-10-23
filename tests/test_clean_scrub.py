"""Lane C: the scrubbed environment and the pins of every Git child (T012).

FR-054; design D6, D9 and D11; contracts/project-clean.md, "Git children";
lead rulings R-21, R-23, R-25 and R-28. The push kind follows draft PR #19
(LQ-3, an assumption until Brett Heap's word). The fourteen trace names and
the three trace2 variables at "0" follow Brett Heap's ruling Q9 B, which
draft PR #19 records in change 1's Environment paragraph and its scenario
"Trace targets are never written" (lead ruling R-99 (b) and (d)).
"""
import json
import os
from pathlib import Path
import shlex
import sys
import time
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()

# The contract's list, character for character and in its order
# (contracts/project-clean.md, "Git children"), then the fourteen trace names
# of Brett Heap's ruling Q9 B in the order PR #19's Environment paragraph lists
# them, read from Git 2.36.6 to 2.43.7's sources.
SCRUB = tuple("""
GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_CONFIG GIT_CONFIG_PARAMETERS
GIT_CONFIG_COUNT GIT_OBJECT_DIRECTORY GIT_DIR GIT_WORK_TREE
GIT_IMPLICIT_WORK_TREE GIT_GRAFT_FILE GIT_INDEX_FILE GIT_NO_REPLACE_OBJECTS
GIT_REPLACE_REF_BASE GIT_PREFIX GIT_SHALLOW_FILE GIT_COMMON_DIR
GIT_INTERNAL_SUPER_PREFIX GIT_ALLOW_PROTOCOL
GIT_TRACE GIT_TRACE_BARE GIT_TRACE_CURL GIT_TRACE_CURL_NO_DATA
GIT_TRACE_FSMONITOR GIT_TRACE_PACKET GIT_TRACE_PACKFILE GIT_TRACE_PACK_ACCESS
GIT_TRACE_PERFORMANCE GIT_TRACE_REDACT GIT_TRACE_REFS GIT_TRACE_SETUP
GIT_TRACE_SHALLOW GIT_TRACE_WORKING_TREE_ENCODING
""".split())

# The three trace2 targets, set to "0" on every Git child (Q9 B).
TRACE2_OFF = {"GIT_TRACE2": "0", "GIT_TRACE2_EVENT": "0", "GIT_TRACE2_PERF": "0"}

# The seven protocol pins, as the contract spells them, and the status pins:
# the contract's two, then the two stat pins of lead ruling R-102 (LQ-10,
# approved by Brett Heap), then core.ignoreCase=false (Brett Heap's Q1, lead
# R-380).
PROTOCOL = tuple("""
-c protocol.allow=never -c protocol.file.allow=never
-c protocol.ssh.allow=never -c protocol.git.allow=never
-c protocol.http.allow=never -c protocol.https.allow=never
-c protocol.ext.allow=never
""".split())
STATUS = ("-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false",
          "-c", "core.trustctime=true", "-c", "core.checkStat=default", "-c", "core.ignoreCase=false")

# Design D9's removal vector up to `-C`, character for character, with R-102's
# two stat pins after core.fsmonitor=false and Q1's core.ignoreCase=false after
# them (lead R-380).
D9_REMOVAL = """git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -c core.trustctime=true -c core.checkStat=default -c
core.ignoreCase=false -c protocol.allow=never -c protocol.file.allow=never -c
protocol.ssh.allow=never -c protocol.git.allow=never -c
protocol.http.allow=never -c protocol.https.allow=never -c
protocol.ext.allow=never""".split()

KINDS = ("probe", "status", "hidden", "removal", "delegate", "push")
READ_ONLY = ("probe", "status", "hidden")
STATUS_PINNED = ("status", "hidden", "removal")


def holds(argv, part):
    """Whether PART stands in ARGV as one contiguous run."""
    part = list(part)
    return any(argv[i:i + len(part)] == part for i in range(len(argv) - len(part) + 1))


class ScrubTests(unittest.TestCase):
    def test_clean_scrub_removes_the_thirty_one_names(self):
        self.assertEqual(project.GIT_SCRUB, SCRUB)
        self.assertEqual(len(set(SCRUB)), 31)
        # The caller's environment, built whole: all thirty-one, the two config
        # files, the three trace2 targets naming files, another trace2 name,
        # and names the scrub never touches; no GIT_OPTIONAL_LOCKS.
        caller = {name: "caller-" + name for name in SCRUB}
        caller.update(GIT_CONFIG_GLOBAL="/cfg/global", GIT_CONFIG_SYSTEM="/cfg/system",
                      GIT_CONFIG_NOSYSTEM="1", PATH="/usr/bin:/bin",
                      LANE_C_UNRELATED="kept", GIT_TRACE2_BRIEF="1",
                      **{name: "/trace/" + name for name in TRACE2_OFF})
        with mock.patch.dict(os.environ, caller, clear=True):
            self.assertEqual(dict(os.environ), caller)
            envs = {kind: project.git_env(kind) for kind in KINDS}
            self.assertEqual(dict(os.environ), caller)
            envs["probe"]["GIT_DIR"] = "/changed"
            self.assertEqual(dict(os.environ), caller)
            envs["probe"] = project.git_env("probe")
        for kind, env in envs.items():
            with self.subTest(kind=kind):
                kept = ("GIT_ALLOW_PROTOCOL",) if kind == "push" else ()
                expected = {name: value for name, value in caller.items()
                            if name not in SCRUB or name in kept}
                expected.update(TRACE2_OFF)
                if kind in READ_ONLY:
                    expected["GIT_OPTIONAL_LOCKS"] = "0"
                self.assertEqual(env, expected)
                self.assertEqual(env["GIT_CONFIG_GLOBAL"], "/cfg/global")
                self.assertEqual(env["GIT_CONFIG_SYSTEM"], "/cfg/system")
                self.assertEqual(env["LANE_C_UNRELATED"], "kept")
                for name in SCRUB:
                    if name in kept:
                        self.assertEqual(env[name], caller[name])
                    else:
                        self.assertNotIn(name, env)
                # Every kind, the push child's included: the caller's trace2
                # targets give way to "0"; the other trace2 names stay (Q9 B).
                for name, value in TRACE2_OFF.items():
                    self.assertEqual(env[name], value)
                self.assertEqual(env["GIT_TRACE2_BRIEF"], "1")
                if kind not in READ_ONLY:
                    self.assertNotIn("GIT_OPTIONAL_LOCKS", env)
        # The push child keeps GIT_ALLOW_PROTOCOL only: the other thirty go.
        self.assertEqual([name for name in SCRUB if name in envs["push"]],
                         ["GIT_ALLOW_PROTOCOL"])
        # A read-only probe sets GIT_OPTIONAL_LOCKS=0 over a caller's value, and
        # every kind sets the trace2 targets off with none given.
        locked = {"GIT_OPTIONAL_LOCKS": "1", "PATH": "/usr/bin:/bin"}
        with mock.patch.dict(os.environ, locked, clear=True):
            for kind in READ_ONLY:
                self.assertEqual(project.git_env(kind),
                                 {"GIT_OPTIONAL_LOCKS": "0", "PATH": "/usr/bin:/bin", **TRACE2_OFF})
            for kind in KINDS:
                self.assertEqual({name: project.git_env(kind).get(name) for name in TRACE2_OFF},
                                 TRACE2_OFF)
            self.assertEqual(dict(os.environ), locked)
        # An unknown kind fails closed rather than going unscrubbed.
        with self.assertRaises(KeyError):
            project.git_env("unknown")

    def test_clean_pins_are_on_every_argv(self):
        self.assertEqual(project.PROTOCOL_PINS, PROTOCOL)
        self.assertEqual(len(PROTOCOL), 14)
        self.assertEqual(project.STATUS_PINS, STATUS)
        args = ["-C", "/repo", "worktree", "list", "--porcelain", "-z"]
        given = list(args)
        for kind in KINDS:
            with self.subTest(kind=kind):
                argv = project.git_argv(kind, args)
                self.assertEqual(argv[0], "git")
                self.assertEqual(argv[len(argv) - len(args):], args)
                pins = argv[1:len(argv) - len(args)]
                self.assertEqual(holds(pins, PROTOCOL), kind != "push")
                self.assertEqual(holds(pins, STATUS), kind in STATUS_PINNED)
                self.assertEqual("status.showUntrackedFiles=normal" in pins,
                                 kind == "removal")
                expected = (len(PROTOCOL) if kind != "push" else 0) + (
                    len(STATUS) if kind in STATUS_PINNED else 0) + (2 if kind == "removal" else 0)
                self.assertEqual(len(pins), expected)
        self.assertEqual(args, given)
        # The removal: D9's vector exactly, the path one argument of raw bytes.
        path = b"/repo/wt/caf\xc3\xa9 \xff\nx"
        argv = project.git_argv("removal", ["-C", "/repo", "worktree", "remove", path])
        self.assertEqual(argv, [*D9_REMOVAL, "-C", "/repo", "worktree", "remove", path])
        self.assertIs(argv[-1], path)
        self.assertNotIn("--force", argv)
        # A status probe starts as D11 spells it, the protocol pins after.
        status = ["-C", "/repo/wt", "status", "--porcelain=v1", "-z",
                  "--untracked-files=normal", "--ignored=matching"]
        self.assertEqual(project.git_argv("status", status),
                         ["git", *STATUS, *PROTOCOL, *status])
        hidden = ["-C", "/repo/wt", "ls-files", "-v", "--stage", "-z"]
        self.assertEqual(project.git_argv("hidden", hidden),
                         ["git", *STATUS, *PROTOCOL, *hidden])
        # git --version and the delete-branch delegate carry the seven pins.
        self.assertEqual(project.git_argv("probe", ["--version"]),
                         ["git", *PROTOCOL, "--version"])
        branch = ["-C", "/repo", "branch", "-d", "feature"]
        self.assertEqual(project.git_argv("delegate", branch),
                         ["git", *PROTOCOL, *branch])
        # The push child carries no pin at all (draft PR #19).
        push = ["-C", "/repo", "push", "origin", "feature:feature"]
        self.assertEqual(project.git_argv("push", push), ["git", *push])
        with self.assertRaises(KeyError):
            project.git_argv("unknown", args)


class PinnedStatusTests(clean_support.CleanCase):
    """STATUS_PINS's stat pins (R-102: LQ-10, approved by Brett Heap; lane 3's
    F1 H-3), beside its argument-vector test above. Rule 1 names the test after
    the evidence model's scenario "The pinned status configuration"."""

    def test_status_the_pinned_status_configuration_sees_a_same_size_edit(self):
        # A linked worktree whose repository sets core.trustctime=false and
        # core.checkStat=minimal, with a tracked file edited at the same size
        # and its mtime restored: only its ctime tells, which those settings
        # ignore. The status probe's own pins read it, so --all-safe never
        # selects the row.
        root = self.repo()
        self.bare_remote()
        tree = self.merged_worktree("050-edited")
        tracked = tree / "work-050-edited"  # "done", committed and merged
        self.git(root, "config", "core.trustctime", "false")
        self.git(root, "config", "core.checkStat", "minimal")
        before = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(before, 0)
        self.assertEqual([entry["path"] for entry in before.document["selected"]], [str(tree)])

        # The file's mtime set well in the past and recorded in the index, so the
        # entry is not racily clean; then a wait past a whole second, so that the
        # edit's ctime differs from the indexed one without nanosecond stat data.
        old = time.time_ns() - 100 * 10**9
        os.utime(tracked, ns=(old, old))
        self.git(tree, "update-index", "-q", "--refresh")
        time.sleep(1.1)
        tracked.write_text("edit")  # four bytes, as "done" is
        os.utime(tracked, ns=(old, old))
        self.assertEqual(tracked.stat().st_mtime_ns, old)
        # Git under the repository's own settings misses the edit.
        self.assertEqual(self.git(tree, "status", "--porcelain", env=dict(self.env, GIT_OPTIONAL_LOCKS="0")), "")

        after = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(after, 0)
        self.assertEqual(after.document["selected"], [])
        self.assertIn((str(tree), "dirty"), [(entry["path"], entry["reason"]) for entry in after.document["excluded"]])

        # Row 116's THEN (pc:342-344; lane 3's W115 LOW-2): `--all-safe --apply --yes` leaves the
        # worktree and the edit in place. The apply plans afresh with the same pins, so it selects
        # nothing and removes nothing; without them it would remove the worktree and lose the edit.
        applied = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json")
        self.assert_status(applied, 0)
        self.assertEqual((applied.document["selected"], applied.document["operations"]),
                         ([], {"estimated": 0, "performed": 0}), "a plan with no target, and no removal run")
        self.assertTrue(tree.is_dir(), "the worktree is kept")
        self.assertEqual(tracked.read_text(), "edit", "the edit is kept")
        self.assertEqual(tracked.stat().st_mtime_ns, old, "the file is untouched")
        self.assertIn(f"worktree {tree}\n", self.git(root, "worktree", "list", "--porcelain"))
        human = self.run_cli("clean", root, "--all-safe", "--apply", "--yes")
        self.assert_status(human, 0)
        self.assertTrue(tree.is_dir() and tracked.read_text() == "edit")

    # Brett Heap's Q1, "yes, recommended for Q1-Q9" (lead R-380; lane 2's wave 22
    # triage T1; sr-classification H-2, sr-evidence H-1 and H-2, sr-removal F1):
    # core.ignoreCase=false joins the status pins, on the status and hidden-state
    # probes and the removal. Under core.ignoreCase=true on a case-sensitive file
    # system Git hid an untracked case variant, and `git worktree remove PATH`
    # resolved PATH to another worktree whose path differs only in case.

    def test_status_a_case_variant_untracked_file(self):
        # A merged worktree holds an untracked WORK-... beside its tracked
        # work-..., with core.ignoreCase=true read from the repository's config,
        # or from the caller's global configuration alone. Git under that setting
        # lists nothing, so the row read clean, was selected, and the apply
        # deleted the file. The pinned probe lists `?? WORK-...`: the row is
        # dirty, nothing is selected, and the apply keeps the worktree and the file.
        for number, where in enumerate(("the repository's config", "GIT_CONFIG_GLOBAL")):
            with self.subTest(where):
                root = self.repo(f"icase-{number}")
                self.bare_remote(root, name=f"icase-{number}.git")
                tree = self.merged_worktree(f"00{number}-feat", path=self.base / f"icase-{number}-wt", root=root)
                variant = tree / f"WORK-00{number}-FEAT"  # beside the tracked work-00N-feat
                env = dict(self.env)
                if number == 0:
                    self.git(root, "config", "core.ignoreCase", "true")
                else:
                    config = self.base / "icase-global.gitconfig"
                    config.write_text("[core]\n\tignoreCase = true\n")
                    env["GIT_CONFIG_GLOBAL"] = str(config)
                variant.write_text("my unique notes, found nowhere else\n")
                self.assertEqual(self.git(tree, "status", "--porcelain", "--untracked-files=normal", "--ignored",
                                          env=dict(env, GIT_OPTIONAL_LOCKS="0")), "",
                                 "Git under that setting lists nothing")
                preview = self.run_json("clean", root, "--all-safe", "--json", env=env)
                self.assert_status(preview, 0)
                self.assertEqual(preview.document["selected"], [])
                [row] = [row for row in preview.document["worktrees"] if row["path"] == str(tree)]
                self.assertEqual((row["dirty"], row["classification"]), (True, "dirty"))
                self.assertIn((str(tree), "dirty"),
                              [(entry["path"], entry["reason"]) for entry in preview.document["excluded"]])
                applied = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json", env=env)
                self.assert_status(applied, 0)
                self.assertEqual(applied.document["operations"], {"estimated": 0, "performed": 0})
                self.assertTrue(variant.is_file(), "the case-variant file is kept")
                self.assertIn(f"worktree {tree}\n", self.git(root, "worktree", "list", "--porcelain"))

    def test_clean_two_worktree_paths_that_differ_only_in_case(self):
        # Two merged worktrees, wt-x and WT-X, under core.ignoreCase=true. The
        # first in the readdir order of the admin directories, the order Git's
        # find_worktree() tries them in, holds a commit that its HEAD reflog
        # alone holds, so it is excluded as worktree-only-commits; the other is
        # eligible. Git, asked to remove the eligible path, removed the excluded
        # worktree, and its commit with it. The removal's pin makes Git resolve
        # the path to the entry of exactly that spelling: the eligible one is
        # removed, and the excluded one and its commit remain.
        root = self.repo()
        self.bare_remote()
        trees = {"wt-x": self.merged_worktree("001-lower", path=self.base / "wt-x"),
                 "WT-X": self.merged_worktree("002-upper", path=self.base / "WT-X")}
        branches = {"wt-x": "001-lower", "WT-X": "002-upper"}
        order = [name for name in os.listdir(self.common_dir(root) / "worktrees") if name in trees]
        self.assertEqual(sorted(order), sorted(trees))
        held_name, eligible_name = order
        held, eligible = trees[held_name], trees[eligible_name]
        self.git(held, "checkout", "-q", "--detach")
        (held / "precious").write_text("only here")
        commit = self.commit(held, "held only by this worktree's HEAD reflog")
        self.git(held, "checkout", "-q", branches[held_name])
        self.git(root, "config", "core.ignoreCase", "true")
        preview = self.run_json("clean", root, "--all-safe", "--json")
        self.assert_status(preview, 0)
        self.assertEqual([entry["path"] for entry in preview.document["selected"]], [str(eligible)])
        self.assertIn((str(held), "worktree-only-commits"),
                      [(entry["path"], entry["reason"]) for entry in preview.document["excluded"]])
        applied = self.run_json("clean", root, "--all-safe", "--apply", "--yes", "--json")
        self.assert_status(applied, 0)
        self.assertEqual([(target["path"], target["stage"], target["reason"]) for target in applied.document["targets"]],
                         [(str(eligible), "removed", None)])
        self.assertFalse(eligible.exists(), "the eligible worktree is removed")
        self.assertTrue(held.is_dir(), "the excluded worktree remains")
        listed = self.git(root, "worktree", "list", "--porcelain")
        self.assertIn(f"worktree {held}\n", listed)
        self.assertNotIn(f"worktree {eligible}\n", listed)
        self.assertIn(commit, self.git(held, "log", "-g", "--format=%H", "HEAD").split(), "its commit remains")


# The env-dumping git, inline (lead ruling R-99 (d) 2). First on PATH, an sh
# script that execs this Python, which appends one JSON line per child, its
# argument vector and every GIT_* variable it was given, then execs the real
# git by absolute path: the record is the environment that Git itself runs in.
ENV_DUMP = r'''
import json, os, sys
log, real, argv = sys.argv[1], sys.argv[2], sys.argv[3:]
record = {"argv": argv,
          "env": {name: value for name, value in os.environ.items() if name.startswith("GIT_")}}
with open(log, "a") as stream:
    stream.write(json.dumps(record) + "\n")
os.execv(real, [real] + argv)
'''

# The caller's trace variables of PR #19's scenario, each set to a file path.
TRACE_NAMES = ("GIT_TRACE", "GIT_TRACE_PACKET", "GIT_TRACE2", "GIT_TRACE2_EVENT")


class TraceTests(clean_support.CleanCase):
    """Brett Heap's ruling Q9 B, through PR #19's scenario "Trace targets are
    never written" (project-command, the evidence model); rule 1 names each
    test after it. Every trace target named here is a file in an empty
    directory, so a trace written anywhere leaves a file there."""

    def env_dump(self):
        """The env-dumping git first on PATH; returns the environment and its log."""
        bin_dir, log, script = self.base / "env-dump-bin", self.base / "env-dump.jsonl", self.base / "env-dump.py"
        bin_dir.mkdir()
        script.write_text(ENV_DUMP)
        words = (sys.executable, "-I", str(script), str(log), clean_support.REAL_GIT)
        wrapper = bin_dir / "git"
        wrapper.write_text("#!/bin/sh\nexec " + " ".join(map(shlex.quote, words)) + ' "$@"\n')
        wrapper.chmod(0o755)
        log.write_text("")
        return self.path_first(bin_dir), log

    def children(self, log):
        """The env-dumping git's records, one per Git child, in their order."""
        return [json.loads(line) for line in Path(log).read_text().splitlines()]

    def targets(self, directory, *names):
        """An empty directory, and {name: the absolute path of a file in it} per name."""
        directory.mkdir()
        return {name: str(directory / name.lower()) for name in names}

    def global_config(self, path, **settings):
        """A global configuration file at path with each trace2.KEY = VALUE."""
        path.write_text("[trace2]\n" + "".join(f"\t{key} = {json.dumps(value)}\n"
                                               for key, value in settings.items()))
        return str(path)

    def assert_unwritten(self, directory, result=None):
        detail = "" if result is None else "\n" + clean_support.transcript(result)
        self.assertEqual(sorted(os.listdir(directory)), [], "a trace target was written" + detail)

    def test_status_trace_targets_are_never_written(self):
        # PR #19's scenario through the real git: status and clean for a
        # repository with one linked worktree, the caller's four trace
        # variables and the global trace2.eventTarget each naming a file.
        root = self.repo()
        self.git(root, "worktree", "add", "-q", "-b", "030-linked", self.base / "030-linked-tree")
        traces = self.base / "traces"
        env = dict(self.env, **self.targets(traces, *TRACE_NAMES))
        env["GIT_CONFIG_GLOBAL"] = self.global_config(self.base / "global.config",
                                                      eventTarget=str(traces / "config-event"))
        runs = (("status", root), ("clean", root), ("clean", root, "--json"))
        for args in runs:
            with self.subTest(args=args[:1] + args[2:]):
                result = self.run_cli(*args, env=env)
                self.assert_status(result, 0)
                self.assert_unwritten(traces, result)

        with self.subTest("the three trace2 targets in the global configuration, no trace variable"):
            config = self.base / "config-traces"
            config.mkdir()
            env = dict(self.env, GIT_CONFIG_GLOBAL=self.global_config(
                self.base / "targets.config", normalTarget=str(config / "normal"),
                eventTarget=str(config / "event"), perfTarget=str(config / "perf")))
            for args in runs:
                result = self.run_cli(*args, env=env)
                self.assert_status(result, 0)
                self.assert_unwritten(config, result)

    def test_status_trace_targets_are_never_written_by_any_kind_of_child(self):
        # The scenario's wrapper, run over every kind of Git child: status,
        # doctor and the clean report (probes, status and hidden-state probes),
        # an --all-safe apply (the removal), delete-branch (the delegate) and
        # push (the push child), with the caller's four trace variables each
        # naming a file.
        root = self.repo()
        remote = self.bare_remote()
        self.merged_worktree("040-done")
        feature = self.base / "041-feature-tree"
        self.git(root, "worktree", "add", "-q", "-b", "041-feature", feature)
        self.git(feature, "push", "-q", "-u", "origin", "041-feature")
        head = self.commit(feature, "one more", allow_empty=True)
        traces = self.base / "traces"
        env, log = self.env_dump()
        env.update(self.targets(traces, *TRACE_NAMES))
        for args in (("status", root), ("doctor", root), ("clean", root, "--json"),
                     ("clean", root, "--all-safe", "--apply", "--yes"),
                     ("clean", root, "--apply", "--action", "delete-branch", "--branch", "040-done", "--yes"),
                     ("clean", root, "--apply", "--action", "push", "--branch", "041-feature", "--yes")):
            result = self.run_cli(*args, env=env)
            if args[0] != "doctor":  # doctor's exit follows its tool rows, not Git's
                self.assert_status(result, 0)
            self.assert_unwritten(traces, result)

        children = self.children(log)
        for kind, part in (("status", ["status", "--porcelain=v1"]), ("hidden", ["ls-files", "-v"]),
                           ("removal", ["worktree", "remove"]), ("delegate", ["branch", "-d"]),
                           ("push", ["push"])):
            self.assertTrue(any(holds(child["argv"], part) for child in children), f"no {kind} child ran")
        for child in children:
            with self.subTest(argv=child["argv"]):
                self.assertEqual({name: child["env"].get(name) for name in TRACE2_OFF}, TRACE2_OFF)
                self.assertEqual([name for name in SCRUB if name in child["env"]], [])
        self.assertEqual(self.git(remote, "rev-parse", "refs/heads/041-feature").strip(), head)
        self.assertEqual(self.git(root, "branch", "--list", "040-done"), "")


if __name__ == "__main__":
    unittest.main()
