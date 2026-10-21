"""The text lane of feature 004's User Story 5 (T091, for T094): the stop block,
the branches it keeps and the probable partial-removal note (design D4, D18 and
D19; the project-clean delta, "Only tracked-file deletions", "project killed
during a deletion" and "The stop block"; data-model.md, "Target result and
reconciliation record" and "Target stages"; contracts/project-clean.md, "Human
output"; lead rulings R-76 (c), (d) and (f), R-79 (P-10, P-11) and R-83 (P-2)).

The stop block runs `project clean` as a child under the counting wrapper,
whose post-remove hook changes the next target after Git removed the first;
R-76 (f)'s clause calls print_result() in process on literal targets, as the
apply lane's test does. The partial-removal note is pinned twice: by tracked
files deleted by hand (the deterministic gate, D4), and by `project` and its
removal child killed with SIGKILL in the middle of a deletion, run through the
launcher, once before the status probe's record bound and once past it.
Expected human text comes from clean_support's fixtures (rule 8); the baseline
recommendations are written here as literals (rule 11).
"""
import contextlib
import io
import os
from pathlib import Path
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import types
import unittest

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES
STEPS = clean_support.NEXT_STEP_FIXTURES
REAL_GIT = clean_support.REAL_GIT

# The baseline recommendations the scenarios show, written here as literals.
DIRTY_ADVICE = "Preserve or commit the working changes before cleanup."
INSPECTION_ERROR_ADVICE = "Preserve this worktree; Git could not establish its clean state."

SHA_A, SHA_B = "a" * 40, "b" * 40
NOTE = "partially-removed"
# Where the partial-removal note prints (lead ruling R-79, P-11): in the
# report under the row's recommendation, indented as that line is; in the
# preview under the row's `    PATH [BRANCH]` line, two spaces deeper.
REPORT_INDENT, PREVIEW_INDENT = "  ", "      "


def when_target(path, *commands):
    """sh text for a counting-wrapper hook that runs commands only when the
    worktree being removed ($target) is path."""
    return f"if [ \"$target\" = {shlex.quote(os.fsdecode(path))} ]; then\n" + "\n".join(commands) + "\nfi"


def sh_git(*args):
    """One real-git command line for a hook, by absolute path (lead ruling R-31)."""
    return " ".join(shlex.quote(os.fsdecode(arg)) for arg in (REAL_GIT, *args))


def is_removal(record):
    """Whether a counted child is a `worktree remove`, its pins and `-C DIR`
    aside."""
    words = list(record.argv)
    while len(words) > 1 and words[0] == "-c":
        words = words[2:]
    if words[:1] == ["-C"]:
        words = words[2:]
    return words[:2] == ["worktree", "remove"]


def record(registry_entry_present, path_present, branch_present, branch_sha):
    """A reconciliation record, as project builds it (reconciled derived)."""
    return project.reconciliation_record(registry_entry_present, path_present, branch_present, branch_sha)


def literal_target(stage, reason=None, path=b"/w/p1", branch="b1", reconciliation="default", notes=(),
                   exit_status=None):
    """A literal target result as the apply phase keeps it (region apply,
    Target): `path` raw bytes, `command` the planned vector. A
    `not-attempted` target has no reconciliation by default; any other the
    record of a clean removal, its branch read back at its planned SHA."""
    if reconciliation == "default":
        reconciliation = None if stage == "not-attempted" else record(False, False, True, SHA_A)
    return {"path": path, "branch": branch, "planned_sha": SHA_A, "stage": stage, "reason": reason,
            "notes": list(notes), "command": ["git", "-C", b"/r", "worktree", "remove", path],
            "exit_status": exit_status, "probes_performed": 0 if stage == "not-attempted" else 5,
            "reconciliation": reconciliation}


class RaisingStream(io.StringIO):
    """A human stream whose writes fail as a closed pipe's do."""

    def write(self, text):
        raise BrokenPipeError(32, "Broken pipe")


def note_line(path):
    """D18's partial-removal note for path, its command form (lead ruling
    R-83, P-2: the note names a command to paste)."""
    return TEXT["partial_removal_note"].format(PATH=shlex.quote(os.fsdecode(path)))


class StopTests(clean_support.CleanCase):

    def counting(self, hooks=None):
        """The counting wrapper first on PATH, with hooks: (env, log)."""
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        clean_support.install_counting_git(bin_dir, log, hooks=hooks)
        clean_support.reset_child_log(log)
        return self.path_first(bin_dir), log

    def head(self, path, ref="HEAD"):
        return self.git(path, "rev-parse", ref).strip()

    # T091: "The stop block". It pins T057, and R-76 (f)'s clause waits for
    # T094's TEXT key.

    def test_clean_the_stop_block(self):
        # Three merged worktrees P1, P2 and P3 on B1, B2 and B3. The counting
        # wrapper's post-remove hook on P1 commits on B2 in P2 through
        # REAL_GIT, after Git removed P1 and before the rescan, so P2's
        # revalidation refuses it with branch-changed (T084) and P3 is not
        # attempted.
        root = self.repo()
        self.bare_remote()
        names = (("p1", "b1"), ("p2", "b2"), ("p3", "b3"))
        trees = [self.merged_worktree(branch, path=self.base / "trees" / name) for name, branch in names]
        planned = {branch: self.head(root, f"refs/heads/{branch}") for _, branch in names}
        env, log = self.counting({"post": when_target(trees[0], sh_git(
            "-C", trees[1], "commit", "-q", "--allow-empty", "-m", "advance after P1"))})
        result = self.run_cli("clean", root, "--all-safe", "--apply", "--yes", env=env)
        self.assert_status(result, 2)
        transcript = "\n" + clean_support.transcript(result)

        # The human result, in the order R-76 (d) reads D18: one progress line
        # per target in the contract's form, then the stop block with ROOT in
        # its command form, `Branches kept:` naming every retained branch, and
        # the residual-window line.
        progress = [TEXT["progress_line"].format(STAGE="removed", PATH=trees[0]),
                    TEXT["progress_line_reason"].format(STAGE="refused", PATH=trees[1], REASON="branch-changed"),
                    TEXT["progress_line_reason"].format(STAGE="not-attempted", PATH=trees[2],
                                                        REASON="batch-stopped")]
        stop = TEXT["stop_block"].format(PATH=trees[1], REASON="branch-changed", K=1, N=3, NOT_ATTEMPTED=trees[2],
                                         ROOT=shlex.quote(str(root)))
        self.assertEqual(stop, f"Stopped at {trees[1]} (branch-changed). Removed 1 of 3. Not attempted: "
                               f"{trees[2]}. Next: project clean {shlex.quote(str(root))} --all-safe")
        lines = result.stdout.splitlines()
        self.assertEqual(lines[-6:], progress + [stop, TEXT["branches_kept_line"].format(BRANCHES="b1, b2, b3"),
                                                  TEXT["residual_window_line"]], transcript)
        self.assertLess(lines.index(TEXT["selected_heading"].format(N=3)), len(lines) - 6,
                        "the result follows the plan" + transcript)

        # What the run did: one removal, P1's; B2 kept at the commit the hook
        # made; every branch kept; P2 and P3 untouched.
        self.assertEqual(sum(map(is_removal, clean_support.child_log(log))), 1, transcript)
        self.assertFalse(trees[0].exists())
        self.assertTrue(trees[1].is_dir() and trees[2].is_dir())
        self.assertEqual(self.head(root, "refs/heads/b1"), planned["b1"])
        self.assertNotEqual(self.head(root, "refs/heads/b2"), planned["b2"])
        self.assertEqual(self.head(root, "refs/heads/b2"), self.head(trees[1]))
        self.assertEqual(self.head(root, "refs/heads/b3"), planned["b3"])

        # R-76 (f), as T091 words it at 05e6218 and R-79 rules P-10: a branch
        # whose last read shows it absent (branch_present false, at any stage),
        # or that a spawned target's rescan did not read back (branch_present
        # null on a removed, failed or unknown target), is left out of
        # `Branches kept:` and named on one line after it, before the
        # residual-window line, in T094's TEXT key; `Branches kept: none.`
        # when every branch is left out. Refused and not-attempted targets keep
        # their branch, since nothing was spawned for them.
        not_confirmed = TEXT.get("branches_not_confirmed")
        self.assertIsNotNone(not_confirmed, "T094 adds the TEXT key that names the branches left out of "
                                            "Branches kept: (lead ruling R-79, P-10)")
        self.assertEqual(not_confirmed.format(BRANCHES="b2"), "Branches not confirmed: b2.")
        plan = types.SimpleNamespace(root=b"/r oot")
        p1, p2, p3 = (dict(path=f"/w/p{n}".encode(), branch=f"b{n}") for n in (1, 2, 3))
        kept = TEXT["branches_kept_line"]
        residual = TEXT["residual_window_line"]

        def stop_block(path, reason, removed, total, skipped):
            return TEXT["stop_block"].format(PATH=path, REASON=reason, K=removed, N=total, NOT_ATTEMPTED=skipped,
                                             ROOT="'/r oot'")

        later = [literal_target("not-attempted", "batch-stopped", **p2),
                 literal_target("not-attempted", "batch-stopped", **p3)]
        cases = [
            ("branch missing after removal",
             [literal_target("removed", "branch-missing-after-removal", reconciliation=record(False, False, False, None),
                             exit_status=0, **p1), *later],
             [stop_block("/w/p1", "branch-missing-after-removal", 1, 3, "/w/p2, /w/p3"),
              kept.format(BRANCHES="b2, b3"), not_confirmed.format(BRANCHES="b1"), residual]),
            ("never read back after exit 0",
             [literal_target("removed", exit_status=0, **p1),
              literal_target("unknown", "reconciliation-incomplete", reconciliation=record(False, False, None, None),
                             exit_status=0, **p2),
              literal_target("not-attempted", "batch-stopped", **p3)],
             [stop_block("/w/p2", "reconciliation-incomplete", 1, 3, "/w/p3"),
              kept.format(BRANCHES="b1, b3"), not_confirmed.format(BRANCHES="b2"), residual]),
            ("a ceiling target whose rescan established nothing",
             [literal_target("removed", exit_status=0, **p1),
              literal_target("unknown", "removal-ceiling", reconciliation=record(None, None, None, None),
                             exit_status=137, **p2),
              literal_target("not-attempted", "batch-stopped", **p3)],
             [stop_block("/w/p2", "removal-ceiling", 1, 3, "/w/p3"),
              kept.format(BRANCHES="b1, b3"), not_confirmed.format(BRANCHES="b2"), residual]),
            ("failed and never read back, so nothing kept",
             [literal_target("failed", "git-failed", reconciliation=record(True, True, None, None), exit_status=1,
                             **p1)],
             [stop_block("/w/p1", "git-failed", 0, 1, "none"),
              kept.format(BRANCHES="none"), not_confirmed.format(BRANCHES="b1"), residual]),
            ("refused before its ref listing, and not attempted",
             [literal_target("refused", "identity-changed", reconciliation=record(None, True, None, None), **p1),
              *later],
             [stop_block("/w/p1", "identity-changed", 0, 3, "/w/p2, /w/p3"),
              kept.format(BRANCHES="b1, b2, b3"), residual]),
            ("refused with its branch read absent",
             [literal_target("removed", exit_status=0, **p1),
              literal_target("refused", "branch-changed", reconciliation=record(True, True, False, None), **p2),
              literal_target("not-attempted", "batch-stopped", **p3)],
             [stop_block("/w/p2", "branch-changed", 1, 3, "/w/p3"),
              kept.format(BRANCHES="b1, b3"), not_confirmed.format(BRANCHES="b2"), residual]),
            # R-79, P-11: the partial-removal note prints first, one line per
            # partially-removed target, its PATH in the command form (R-83,
            # P-2), before the stop block; the result still ends with the stop
            # block, `Branches kept:` and the residual-window line (R-76 (d)).
            ("partially removed at the ceiling",
             [literal_target("removed", exit_status=0, **p1),
              literal_target("unknown", "removal-ceiling", path=b"/w/p 2", branch="b2", notes=[NOTE],
                             reconciliation=record(True, True, True, SHA_B), exit_status=137),
              literal_target("not-attempted", "batch-stopped", **p3)],
             [TEXT["partial_removal_note"].format(PATH="'/w/p 2'"),
              stop_block("/w/p 2", "removal-ceiling", 1, 3, "/w/p3"),
              kept.format(BRANCHES="b1, b2, b3"), residual]),
        ]
        for name, targets, expected in cases:
            with self.subTest(case=name):
                run = types.SimpleNamespace(human=io.StringIO(), write_error=None)
                project.print_result(plan, targets, run)
                self.assertEqual(run.human.getvalue().splitlines(), expected)
                self.assertIsNone(run.write_error)

        # Every line goes through say(): a failed write is recorded, never raised.
        run = types.SimpleNamespace(human=RaisingStream(), write_error=None)
        project.print_result(plan, cases[-1][1], run)
        self.assertIsInstance(run.write_error, BrokenPipeError)

    # T091: "Only tracked-file deletions", D4's deterministic gate. The JSON
    # row note pins T032; the human note is T094's.

    def test_clean_only_tracked_file_deletions(self):
        root = self.repo()
        self.bare_remote()

        def tracked_files(tree):
            # Names of this worktree's own, since each later worktree starts at
            # the merge target, which holds the earlier ones' files.
            own = tree.name.replace(" ", "-")
            for name in ("a.txt", "b.txt"):
                (tree / f"{own}-{name}").write_text(name)
            (tree / f"{own}-sub").mkdir()
            (tree / f"{own}-sub" / "c.txt").write_text("c")

        # A path holding a space, so that the note's command form is quoted
        # (lead ruling R-83, P-2) while the row prints its prose form.
        gone = self.merged_worktree("001-gone", path=self.base / "gone tree", setup=tracked_files)
        mixed = self.merged_worktree("002-mixed", path=self.base / "mixed-tree", setup=tracked_files)
        # Every tracked file of `gone` deleted by hand; its `.git` file intact.
        for path in sorted(gone.rglob("*"), reverse=True):
            if path == gone / ".git":
                continue
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()
        self.assertEqual(sorted(path.name for path in gone.iterdir()), [".git"])
        # One deleted tracked file and one untracked file: no note.
        (mixed / "mixed-tree-a.txt").unlink()
        (mixed / "untracked").write_text("new")

        document = self.run_json("clean", root, "--json").document
        rows = {row["path"]: row for row in document["worktrees"]}
        self.assertEqual([(rows[str(path)]["classification"], rows[str(path)]["dirty"], rows[str(path)]["notes"])
                          for path in (root, gone, mixed)],
                         [("protected-default", False, []), ("dirty", True, [NOTE]), ("dirty", True, [])])
        self.assertEqual([rows[str(path)]["recommendation"] for path in (gone, mixed)], [DIRTY_ADVICE] * 2)

        # The report: the note on its own line, beside the dirty advice and
        # never instead of it, under the row's recommendation (R-79, P-11).
        report = self.run_cli("clean", root)
        self.assert_status(report, 0)
        lines = report.stdout.splitlines()
        transcript = "\n" + clean_support.transcript(report)
        [at] = [index for index, line in enumerate(lines) if line.startswith(f"DIRTY: {gone} [001-gone] ")]
        self.assertEqual(lines[at + 1:at + 3], [REPORT_INDENT + DIRTY_ADVICE, REPORT_INDENT + note_line(gone)],
                         transcript)
        self.assertEqual(note_line(gone), "Probable partial removal: inspect, then git worktree remove --force "
                                          f"'{gone}' by hand.")
        [at] = [index for index, line in enumerate(lines) if line.startswith(f"DIRTY: {mixed} [002-mixed] ")]
        self.assertEqual(lines[at + 1], REPORT_INDENT + DIRTY_ADVICE, transcript)
        self.assertEqual([line for line in lines if "Probable partial removal" in line],
                         [REPORT_INDENT + note_line(gone)], transcript)

        # The --all-safe preview: the note right after the dirty row's line,
        # under its group's dirty advice (R-79, P-11); nothing is selected.
        preview = self.run_cli("clean", root, "--all-safe")
        self.assert_status(preview, 0)
        lines = preview.stdout.splitlines()
        at = lines.index(TEXT["excluded_heading"].format(M=3))
        self.assertEqual(lines[at:], [
            TEXT["excluded_heading"].format(M=3),
            TEXT["excluded_group"].format(REASON="main-worktree", K=1, NEXT_STEP=STEPS["main-worktree"]),
            TEXT["excluded_row"].format(PATH=root, BRANCH="main"),
            TEXT["excluded_group"].format(REASON="dirty", K=2, NEXT_STEP=STEPS["dirty"]),
            TEXT["excluded_row"].format(PATH=gone, BRANCH="001-gone"),
            PREVIEW_INDENT + note_line(gone),
            TEXT["excluded_row"].format(PATH=mixed, BRANCH="002-mixed"),
            TEXT["empty_line"]], "\n" + clean_support.transcript(preview))


class KilledDuringDeletionTests(clean_support.CleanCase):
    """T091's "project killed during a deletion" (design D4): a worktree of
    about 8,000 tracked files, its repository built once per class as a
    template, and each run given its own copy of it and its own worktree."""

    FILES = 8000  # tracked files, every one in the worktree's top directory
    ENTRIES = FILES + 1  # with the `.git` file

    @classmethod
    def setUpClass(cls):
        """The template: a repository whose `main` merged branch `feat`, which
        holds FILES tracked files and is published to a bare `remote.git`.
        `feat` is created at the first commit and then moved to the commit of
        the files, so its reflog shows movement (D10) and its row is
        merged-removable once checked out; the merge is `-s ours`, an ancestry
        proof that keeps the main worktree's checkout empty, so each copy is
        quick. The tree is written by `mktree`, with no file written here."""
        super().setUpClass()
        holder = tempfile.TemporaryDirectory()
        cls.addClassCleanup(holder.cleanup)
        cls.template = Path(holder.name).resolve()
        env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
               "HOME": str(cls.template), **clean_support.AUTHOR}
        for name in (*clean_support.SCRUBBED_NAMES, clean_support.OPTIONAL_LOCKS):
            env.pop(name, None)

        def git(*args, input=None):
            result = subprocess.run([REAL_GIT, *map(os.fsdecode, args)], env=env, input=input, capture_output=True,
                                    text=True, timeout=clean_support.TIMEOUT)
            if result.returncode != 0:
                raise AssertionError(f"template: git {args} exited {result.returncode}\n{result.stderr}")
            return result.stdout.strip()

        repo, remote = cls.template / "repo", cls.template / "remote.git"
        git("init", "-q", "-b", "main", repo)
        git("-C", repo, "commit", "-q", "--allow-empty", "-m", "initial")
        first = git("-C", repo, "rev-parse", "HEAD")
        blob = git("-C", repo, "hash-object", "-w", "--stdin", input="tracked\n")
        tree = git("-C", repo, "mktree", input="".join(f"100644 blob {blob}\tf{number:05d}\n"
                                                       for number in range(cls.FILES)))
        files = git("-C", repo, "commit-tree", tree, "-p", first, "-m", f"{cls.FILES} tracked files")
        git("-C", repo, "branch", "feat", first)
        git("-C", repo, "update-ref", "-m", f"commit: {cls.FILES} tracked files", "refs/heads/feat", files, first)
        git("init", "-q", "--bare", remote)
        git("-C", repo, "remote", "add", "origin", remote)
        git("-C", repo, "push", "-q", "origin", "feat")
        git("-C", repo, "branch", "-q", "-u", "origin/feat", "feat")
        git("-C", repo, "merge", "-q", "--no-ff", "-s", "ours", "feat", "-m", "merge feat")

    def copy_template(self, case):
        """This case's own repository and worktree: BASE/CASE/repo and
        BASE/CASE/remote.git copied from the template, then `feat` checked out
        at BASE/CASE/tree. Returns (root, tree)."""
        top = self.base / case
        root = top / "repo"
        shutil.copytree(self.template / "repo", root, symlinks=True)
        shutil.copytree(self.template / "remote.git", top / "remote.git", symlinks=True)
        self.git(root, "remote", "set-url", "origin", top / "remote.git")
        tree = top / "tree"
        self.git(root, "worktree", "add", "-q", tree, "feat")
        self.assertEqual(len(os.listdir(tree)), self.ENTRIES)
        return root, tree

    @staticmethod
    def gone(pid):
        """Whether process pid has ended: no /proc entry, or a zombie. Without
        /proc (a local run off Linux), a pause stands in for the check."""
        if not os.path.isdir("/proc"):
            time.sleep(0.5)
            return True
        try:
            state = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[0]
        except (FileNotFoundError, ProcessLookupError, IndexError):
            return True
        return state in ("Z", "X")

    def kill_mid_deletion(self, root, tree, target):
        """Run `project clean ROOT --all-safe --apply --yes` through the
        launcher, in a session of its own, under the counting wrapper; once
        its removal child is recorded, hold that child's process group with
        SIGSTOP and let it run in short SIGCONT bursts, polling the
        worktree's remaining entries, until at least target entries are gone;
        then SIGKILL `project`, then the removal child's group, which is still
        stopped, so nothing more is deleted. SIGSTOP and SIGCONT pace the
        removal child only; no signal reaches the test process (rule 7).
        Returns the count of tracked files deleted and whether the `.git`
        file survived."""
        bin_dir, log = self.base / "counting-bin", self.base / "children.log"
        if bin_dir.exists():
            shutil.rmtree(bin_dir)
        clean_support.install_counting_git(bin_dir, log)
        clean_support.reset_child_log(log)
        # The real table through the launcher (lead ruling R-29), recorded as
        # the test's own: a probe budget of TIMING["probe_budget"], 5 s per
        # child, inside the 60 s deadline; the removal itself has no budget.
        table = clean_support.timing_table()
        self.assertEqual(table["probe_budget"], 5)
        argv = clean_support.launched_argv(table, "clean", root, "--all-safe", "--apply", "--yes")
        out_path, err_path = tree.parent / "kill.stdout", tree.parent / "kill.stderr"

        def remaining():
            try:
                return len(os.listdir(tree))
            except FileNotFoundError:
                return 0

        def transcript():
            return (f"\n--- stdout ---\n{out_path.read_text(errors='replace')}"
                    f"\n--- stderr ---\n{err_path.read_text(errors='replace')}")

        group = removal = None
        with open(out_path, "wb") as out, open(err_path, "wb") as err:
            child = subprocess.Popen(argv, cwd=self.base, env=self.path_first(bin_dir), stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, start_new_session=True)
        try:
            deadline = time.monotonic() + 15
            while removal is None:
                removal = next((entry for entry in clean_support.child_log(log) if is_removal(entry)), None)
                if removal is None:
                    if child.poll() is not None:
                        self.fail(f"project exited {child.returncode} before its removal child started"
                                  + transcript())
                    if time.monotonic() > deadline:
                        self.fail("no removal child within 15 s" + transcript())
                    time.sleep(0.001)
            group = removal.pgid
            os.killpg(group, signal.SIGSTOP)
            burst, deleted = 0.0005, self.ENTRIES - remaining()
            while deleted < target:
                if self.gone(removal.pid) or child.poll() is not None:
                    self.fail(f"the removal ended before {target} deletions ({deleted} done)" + transcript())
                if time.monotonic() > deadline:
                    self.fail(f"{deleted} deletions in 15 s, short of {target}" + transcript())
                os.killpg(group, signal.SIGCONT)
                time.sleep(burst)
                os.killpg(group, signal.SIGSTOP)
                now = self.ENTRIES - remaining()
                step, deleted = now - deleted, now
                if step > 250:
                    burst = max(burst / 2, 0.0001)
                elif step < 60:
                    burst = min(burst * 1.5, 0.005)
            os.killpg(child.pid, signal.SIGKILL)  # project, alone in its session
            os.killpg(group, signal.SIGKILL)  # the removal child's group, Git and any child of its own
            self.assertEqual(child.wait(timeout=clean_support.TIMEOUT), -signal.SIGKILL)
            stop = time.monotonic() + 5
            while not self.gone(removal.pid):
                self.assertLess(time.monotonic(), stop, "the removal child outlived SIGKILL")
                time.sleep(0.01)
        finally:
            if child.poll() is None:
                with contextlib.suppress(OSError):
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait()
            if group is not None:
                with contextlib.suppress(OSError):
                    os.killpg(group, signal.SIGKILL)
        survived = (tree / ".git").is_file()
        left = remaining()
        self.assertGreater(left, 0, "the worktree's directory itself remains")
        # Git deletes the admin directory only after the worktree's files, so
        # the registry still lists the tree: the kill came mid-deletion.
        self.assertIn(f"worktree {tree}\n", self.git(root, "worktree", "list", "--porcelain"))
        return self.FILES - (left - (1 if survived else 0)), survived

    def test_clean_project_killed_during_a_deletion(self):
        # Once with fewer deletions than the status probe's record bound
        # (LIMITS["status_records"], 4,096) and once with more, so the second
        # report judges the stream on the prefix it read (D4; pcl:138). Which
        # of the scenario's two cases each run reaches is the readdir order's:
        # the assertions follow the surviving `.git` file.
        bound = project.LIMITS["status_records"]
        self.assertEqual(bound, 4096)
        for case, target, below in (("before-the-bound", 1500, True), ("past-the-bound", 5500, False)):
            with self.subTest(case=case):
                root, tree = self.copy_template(case)
                deleted, survived = self.kill_mid_deletion(root, tree, target)
                if below:
                    self.assertTrue(0 < deleted < bound, deleted)
                else:
                    self.assertTrue(bound < deleted < self.FILES, deleted)
                # Which case this run reached, for the person reading the run.
                print(f"\n{self.id()} [{case}]: {deleted} tracked files deleted at the kill; "
                      f"the .git file {'survived' if survived else 'was deleted'}", file=sys.stderr, flush=True)

                document = self.run_json("clean", root, "--json").document
                row = {entry["path"]: entry for entry in document["worktrees"]}[str(tree)]
                report = self.run_cli("clean", root)
                preview = self.run_cli("clean", root, "--all-safe")
                lines = report.stdout.splitlines()
                shown = preview.stdout.splitlines()
                transcript = "\n" + clean_support.transcript(report) + "\n" + clean_support.transcript(preview)
                if survived:
                    # `dirty`, with the dirty advice and, beside it, the probable
                    # partial-removal note and its recovery text; past the bound
                    # the status stream stopped at it and was judged on its prefix.
                    self.assertEqual((row["classification"], row["dirty"], row["notes"]), ("dirty", True, [NOTE]))
                    self.assertEqual(row["ignored_files_truncated"], not below)
                    self.assert_status(report, 0)
                    [at] = [index for index, line in enumerate(lines) if line.startswith(f"DIRTY: {tree} [feat] ")]
                    self.assertEqual(lines[at + 1:at + 3], [REPORT_INDENT + DIRTY_ADVICE,
                                                            REPORT_INDENT + note_line(tree)], transcript)
                    self.assert_status(preview, 0)
                    at = shown.index(TEXT["excluded_group"].format(REASON="dirty", K=1, NEXT_STEP=STEPS["dirty"]))
                    self.assertEqual(shown[at + 1:at + 3], [TEXT["excluded_row"].format(PATH=tree, BRANCH="feat"),
                                                            PREVIEW_INDENT + note_line(tree)], transcript)
                else:
                    # `registration-mismatch` with classification
                    # `inspection-error`, a named manual remedy and no note.
                    self.assertEqual((row["classification"], row["notes"]), ("inspection-error", []))
                    self.assertIn({"path": str(tree), "reason": "registration-mismatch"},
                                  [{"path": entry["path"], "reason": entry["reason"]}
                                   for entry in document["excluded"]])
                    [at] = [index for index, line in enumerate(lines)
                            if line.startswith(f"INSPECTION-ERROR: {tree} [")]
                    self.assertEqual(lines[at + 1], REPORT_INDENT + INSPECTION_ERROR_ADVICE, transcript)
                    self.assert_status(preview, 1)
                    at = shown.index(TEXT["excluded_group"].format(REASON="registration-mismatch", K=1,
                                                                   NEXT_STEP=STEPS["registration-mismatch"]))
                    self.assertEqual(shown[at + 1], TEXT["excluded_row"].format(PATH=tree, BRANCH="feat"), transcript)
                    for text in (report.stdout, preview.stdout):
                        self.assertNotIn("Probable partial removal", text, transcript)


if __name__ == "__main__":
    unittest.main()
