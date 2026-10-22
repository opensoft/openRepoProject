"""Clean resolves its target Git-first (feature 004, User Story 7: T104 to
T106, the tests of T107 and T108).

Sources: the project-clean delta's requirement "Clean resolves its target
Git-first" (openspec/changes/add-project-clean-all-safe/, which governs),
specs/004-project-clean-all-safe/contracts/project-clean.md ("Resolution",
"Order of a run", "Codes" and "Git children"), data-model.md ("Repository
identity" and "Merge target") and research.md R13; lead rulings R-13 (M15),
R-51, R-53 (P-10 to P-13, P-20), R-56 and R-71 (b). Expected human text comes
from clean_support's fixtures (rule 8); key lists are literals written here
(rule 11). Every repository is a disposable fixture under the test's temporary
directory (rule 4). Removal-dependent clauses wait for the US1 apply lane's
phase 2; until then an apply that gets past check_plan() removes nothing.
"""
import builtins
import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

# The lead's extension of Brett Heap's ruling LQ-15 (lead ruling R-102), which
# Brett Heap may strike: the two variables tested beside HOME and
# XDG_CONFIG_HOME. Striking it here is this one line, made `()`.
EXTENSION = ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM")

EXTENDED_ERROR_KEYS = ["error", "code", "schema_version", "observed_at", "mode", "repository", "merge_target",
                       "completeness", "apply_allowed", "refusals"]
REPOSITORY_KEYS = ["root", "common_dir", "dev", "ino", "root_valid_utf8", "common_dir_valid_utf8"]
MIB = 1048576  # LIMITS["manifest_bytes"], written here as a literal (rule 11)

# The children of D6's table, after `-C DIR` (contracts/project-clean.md, "Git children").
ROW_2 = ["rev-parse", "--show-toplevel"]
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]
# Row 3b (#19's round (i) at e0c91bb, design.md D6 :333): only on a target-not-repository-root
# refusal, where row 3 failed and the directory holds its own .git.
ROW_3B = ["rev-parse", "--path-format=absolute", "--git-dir", "--git-common-dir", "--is-bare-repository"]


def command(record):
    """A counted child's argument vector without its leading -c pins: `-C DIR ...`."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


def config_lines(*names):
    """D18's relative-config-path text for names, one line each, from the fixtures (rule 8)."""
    return "\n".join(TEXT["relative_config_path"].format(NAME=name) for name in names)


def manifest_text(size, *lines):
    """A manifest of exactly size bytes: lines, then comment lines as padding."""
    head = "".join(line + "\n" for line in lines)
    rest = size - len(head)
    assert rest >= 2, rest
    pad = []
    while rest > 0:
        width = min(rest, 4096)
        pad.append("#" * (width - 1) + "\n")
        rest -= width
    text = head + "".join(pad)
    assert len(text.encode()) == size, len(text.encode())
    return text


@contextlib.contextmanager
def working_directory(path):
    """chdir for an in-process run, restored after (contextlib.chdir is 3.11+)."""
    before = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(before)


class ResolutionTests(clean_support.CleanCase):

    # Helpers of this module's own (rule 3's exceptions).

    def main_in_process(self, *argv, cwd=None, **patches):
        """project's main(ARGV) in this process, in self.env and cwd (self.base by
        default), each named function of project replaced by its stand-in:
        (status, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.dict(os.environ, self.env, clear=True))
            stack.enter_context(working_directory(self.base if cwd is None else cwd))
            for name, stand_in in patches.items():
                stack.enter_context(mock.patch.object(project, name, stand_in, create=name == "open"))
            stack.enter_context(contextlib.redirect_stdout(out))
            stack.enter_context(contextlib.redirect_stderr(err))
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def counted(self, *args, cwd=None, env=None):
        """`project ARGS...` under the counting wrapper: the run, its parsed
        document as `document` (None when standard output is not one JSON
        document) and its children."""
        bin_dir = self.base / "counting-bin"
        log = self.base / "children.log"
        clean_support.install_counting_git(bin_dir, log)
        clean_support.reset_child_log(log)
        result = self.run_cli(*args, cwd=cwd, env=self.path_first(bin_dir, env))
        try:
            result.document = json.loads(result.stdout)
        except ValueError:
            result.document = None
        return result, clean_support.child_log(log)

    def snapshot(self, *roots):
        """What a run must leave unchanged: each repository's registry, every
        ref, and every file of its worktrees with its content."""
        state = []
        for root in roots:
            registry = self.git(root, "worktree", "list", "--porcelain")
            trees = [Path(line[9:]) for line in registry.splitlines() if line.startswith("worktree ")]
            files = {}
            for tree in trees:
                for directory, names, filenames in os.walk(tree):
                    names[:] = [name for name in names if name != ".git"]
                    for name in filenames:
                        path = Path(directory) / name
                        if name != ".git" and path.name != "index":
                            files[str(path)] = path.read_bytes()
            state.append((registry, self.git(root, "for-each-ref", "--format=%(refname) %(objectname)"), files))
        return state

    def repository(self, root, common_dir=None):
        """The envelope's `repository` for root, its four identity fields read
        here: `dev` and `ino` by os.lstat of the common directory."""
        common = Path(common_dir) if common_dir is not None else Path(root) / ".git"
        found = os.lstat(common)
        return {"root": str(root), "common_dir": str(common), "dev": found.st_dev, "ino": found.st_ino,
                "root_valid_utf8": True, "common_dir_valid_utf8": True}

    def assert_no_plan(self, records):
        """No row was probed and nothing was acted on: no status or ls-files
        probe, no removal, push or branch deletion."""
        acted = [command(record)[2:] for record in records
                 if command(record)[2:3] in (["status"], ["ls-files"], ["push"], ["branch"])
                 or command(record)[2:4] == ["worktree", "remove"]]
        self.assertEqual(acted, [], "no row probed and nothing acted on before the refusal")

    def assert_error_document(self, result, code, message, mode, repository=None, merge_target=None, path=None):
        """Exit 2 and standard output one extended error object, as
        write_document() writes it (contracts/project-clean.md)."""
        self.assert_status(result, 2)
        document = result.document if hasattr(result, "document") else self.load_json(result)
        self.assertIsNotNone(document, clean_support.transcript(result))
        self.assertEqual(result.stdout, json.dumps(document, indent=2, ensure_ascii=True) + "\n")
        refusal = {"code": code, "message": message}
        if path is not None:
            refusal.update(path=str(path), path_valid_utf8=True)
        self.assertEqual(list(document), EXTENDED_ERROR_KEYS)
        self.assertEqual(document, {
            "error": message, "code": code, "schema_version": 1, "observed_at": document["observed_at"],
            "mode": mode, "repository": repository, "merge_target": merge_target,
            "completeness": "incomplete", "apply_allowed": False, "refusals": [refusal]})
        if repository is not None:
            self.assertEqual(list(document["repository"]), REPOSITORY_KEYS)
        return document

    def assert_refused_human(self, result, message):
        self.assert_status(result, 2)
        self.assertEqual((result.stdout, result.stderr), ("", f"REFUSED: {message}\n"))

    def not_root(self, path):
        return TEXT["target_not_repository_root"].format(PATH=path)

    # T104: "Absolute path that is not a repository root".

    def test_clean_absolute_path_that_is_not_a_repository_root(self):
        root = self.repo()
        self.bare_remote()
        linked = self.merged_worktree("001-merged")
        subdirectory = root / "sub"
        subdirectory.mkdir()
        outside = self.base / "outside"
        outside.mkdir()
        bare = self.base / "remote.git"  # the bare remote itself: a bare repository
        before = self.snapshot(root, bare)
        modes = (
            ("report", (), True),
            ("all-safe", ("--all-safe", "--apply", "--yes"), True),
            ("single", ("--apply", "--action", "remove", "--worktree", linked, "--yes"), True),
            ("single", ("--apply", "--action", "push", "--branch", "001-merged", "--yes"), False),
            ("single", ("--apply", "--action", "delete-branch", "--branch", "001-merged", "--yes"), False),
        )
        for label, path in (("a subdirectory of the root", subdirectory), ("a linked worktree", linked),
                            ("a directory outside any repository", outside), ("a bare repository", bare)):
            message = self.not_root(path)
            for mode, words, json_too in modes:
                with self.subTest(label, words=words[:3]):
                    result, records = self.counted("clean", path, *words)
                    self.assert_refused_human(result, message)
                    self.assert_no_plan(records)
                    self.assertNotIn(ROW_2, [command(record)[2:] for record in records],
                                     "a path takes no name lookup and no redirection")
                    if json_too:
                        result, records = self.counted("clean", path, *words, "--json")
                        self.assert_error_document(result, "target-not-repository-root", message, mode, path=path)
                        self.assert_no_plan(records)
        self.assertEqual(self.snapshot(root, bare), before, "nothing changes")
        with self.subTest("row 3 timed out (P-20)"):
            timeout = {"code": "probe-timeout", "message": "git rev-parse timed out after 5 s"}
            status, out, err = self.main_in_process("clean", root, "--json",
                                                    identity_probe=lambda directory, run: (None, timeout))
            result = mock.Mock(returncode=status, stdout=out, stderr=err, args=["clean", root, "--json"])
            result.document = json.loads(out)
            self.assert_error_document(result, "target-not-repository-root", self.not_root(root), "report", path=root)
        with self.subTest("the main worktree root itself resolves"):
            document = self.run_json("clean", root, "--json").document
            self.assertEqual((document["root"], document["repository"]),
                             (str(root), self.repository(root)))

    # T104: "Overview handoff keeps identity".

    def test_clean_overview_handoff_keeps_identity(self):
        # In process, projects_dirs() patched to two directories, since macOS
        # folds ~/projects and ~/Projects into one.
        first, second = self.base / "projects-one", self.base / "projects-two"
        atlas = self.repo("projects-one/Atlas")
        self.bare_remote(root=atlas)
        tree = self.merged_worktree("001-merged", root=atlas)
        other = second / "Atlas"
        self.git(self.base, "clone", "-q", atlas, other)
        dirs = lambda: [first, second]  # noqa: E731
        spellings = (os.fsencode(other), str(other))

        def children(spy):
            argvs = [call.args[0][1] for call in spy.call_args_list]
            spy.reset_mock()
            return argvs

        holders = (("an ancestor of the Atlas root holds project.yaml", first / "project.yaml", "project-manifest"),
                   ("the root contains Atlas/family.yaml", atlas / "Atlas" / "family.yaml", "family-manifest"))
        for label, holder, kind in holders:
            with self.subTest(label):
                holder.parent.mkdir(exist_ok=True)
                holder.write_text(f"kind: {kind}\n")
                with mock.patch.object(project, "run_bounded", wraps=project.run_bounded) as spy:
                    status, out, err = self.main_in_process("clean", atlas, "--all-safe", "--json",
                                                            projects_dirs=dirs)
                    self.assertEqual((status, err), (0, ""), out)
                    document = json.loads(out)
                    self.assertEqual(document["repository"], self.repository(atlas))
                    self.assertEqual(document["root"], str(atlas))
                    self.assertEqual([entry["path"] for entry in document["selected"]], [str(tree)])
                    argvs = children(spy)
                    self.assertNotIn(ROW_2, [argv[2:] for argv in argvs], "a path takes no name lookup")
                    self.assertEqual([argv for argv in argvs if any(
                        isinstance(word, (bytes, str)) and any(spelled in word for spelled in spellings
                                                               if type(spelled) is type(word)) for word in argv)],
                        [], "no child names the other clone")
                    self.assertNotIn(str(other), out)
                    status, out, err = self.main_in_process("clean", atlas, "--json", projects_dirs=dirs)
                    self.assertEqual((status, err), (0, ""), out)
                    self.assertEqual(json.loads(out)["root"], str(atlas), "the read-only report's root")
                    children(spy)  # reset the spy for the next holder
                if kind == "project-manifest":
                    # Without the family holder the bare name keeps the lookup.
                    status, out, err = self.main_in_process("clean", "Atlas", "--all-safe", projects_dirs=dirs)
                    self.assertEqual((status, out, err), (2, "", "REFUSED: Ambiguous project name; supply a path.\n"))
                    status, out, err = self.main_in_process("clean", "Atlas", "--all-safe", "--json",
                                                            projects_dirs=dirs)
                    result = mock.Mock(returncode=status, stdout=out, stderr=err, args=["clean", "Atlas"])
                    result.document = json.loads(out)
                    self.assert_error_document(result, "ambiguous-name", "Ambiguous project name; supply a path.",
                                               "all-safe")
                else:
                    # P-11: the family holder the name lookup returns is no worktree toplevel.
                    status, out, err = self.main_in_process("clean", "Atlas", "--all-safe", projects_dirs=dirs)
                    self.assertEqual((status, out, err),
                                     (2, "", f"REFUSED: {self.not_root(atlas / 'Atlas')}\n"))
                holder.unlink()

    # T104: research.md R13 as plan review M15 words it.

    def test_clean_bare_name_predicate(self):
        with mock.patch.dict(os.environ, {"HOME": str(self.base)}):
            for argument, bare in (("Atlas", True), ("a b", True), (".", False), ("..", False), ("a/b", False),
                                   ("./a", False), ("a/", False), (str(self.base / "Atlas"), False),
                                   ("~", False), ("~/Atlas", False), ("", False)):
                with self.subTest(argument=argument):
                    self.assertIs(project.is_bare_name(argument), bare)
        # Every relative argument holding a `/` resolves as a path, against the
        # working directory, never through the name lookup; `~` is expanded first.
        atlas = self.repo("Atlas")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        document = self.run_json("clean", "Atlas", "--json", cwd=elsewhere).document
        self.assertEqual(document["root"], str(atlas), "the bare name goes through the projects directory")
        for argument in ("Atlas/", "./Atlas"):
            with self.subTest(argument=argument):
                result = self.run_json("clean", argument, "--json", cwd=elsewhere)
                self.assert_error_document(result, "target-not-repository-root",
                                           self.not_root(elsewhere / "Atlas"), "report", path=elsewhere / "Atlas")
                document = self.run_json("clean", argument, "--json", cwd=self.base).document
                self.assertEqual(document["root"], str(atlas))
        env = dict(self.env, HOME=str(self.base))
        document = self.run_json("clean", "~/Atlas", "--json", cwd=elsewhere, env=env).document
        self.assertEqual(document["root"], str(atlas), "~ is expanded first")

    def test_clean_bare_name_refusals_carry_their_codes(self):
        # P-10: discover()'s bare-name refusals, coded by their baseline messages
        # until US9's T118 codes them in discover() itself.
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        missing = f"Directory does not exist: {elsewhere / 'Nowhere'}"
        result = self.run_json("clean", "Nowhere", "--json", cwd=elsewhere)
        self.assert_error_document(result, "repository-not-found", missing, "report")
        plain = self.base / "Plain"
        plain.mkdir()
        result = self.run_json("clean", "Plain", "--all-safe", "--json", cwd=elsewhere)
        self.assert_error_document(result, "repository-not-found",
                                   f"No project found at {plain}; supply a path or name.", "all-safe")
        result = self.run_cli("clean", "Nowhere", cwd=elsewhere)
        self.assert_refused_human(result, missing)
        coded = project.Refused("Ambiguous project name; supply a path.", code="ambiguous-name")

        def already_coded(target=None):
            raise coded
        status, out, err = self.main_in_process("clean", "Atlas", cwd=elsewhere, discover=already_coded)
        self.assertEqual((status, coded.code), (2, "ambiguous-name"), "a coded refusal passes unchanged")

    def main_in_a_gone_directory(self, *argv):
        """main_in_process() run from a working directory removed after the
        chdir into it: (status, stdout, stderr)."""
        gone = self.base / "gone"
        gone.mkdir()
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, self.env, clear=True), working_directory(gone), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            gone.rmdir()
            status = project.main([os.fspath(arg) for arg in argv])
        return status, out.getvalue(), err.getvalue()

    def document_of(self, status, out, err, argv):
        result = mock.Mock(returncode=status, stdout=out, stderr=err, args=list(argv))
        result.document = json.loads(out)
        return result

    def test_clean_bare_name_refusals_carry_their_codes_for_a_name_the_lookup_cannot_examine(self):
        # The contract's Codes table: `repository-not-found` for "a bare name
        # resolves to no project directory". Plan review F4 (`~user` for no such
        # user: Path.expanduser() raises RuntimeError) and lane 3's US7/US9 L-1
        # (a name of 256 bytes or more: ENAMETOOLONG on Python 3.10 to 3.13) and
        # L-3 (a working directory that is gone) ended in internal-error.
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        for label, name in (("~ for no such user", "~nosuchuser7f3a9c"), ("a name of 300 bytes", "n" * 300)):
            with self.subTest(label):
                message = f"Directory does not exist: {elsewhere / name}"
                result = self.run_json("clean", name, "--json", cwd=elsewhere)
                self.assert_error_document(result, "repository-not-found", message, "report")
                result = self.run_cli("clean", name, "--all-safe", cwd=elsewhere)
                self.assert_refused_human(result, message)
        with self.subTest("a name looked up from a working directory that is gone"):
            argv = ("clean", "Nowhere", "--json")
            result = self.document_of(*self.main_in_a_gone_directory(*argv), argv)
            self.assert_error_document(result, "repository-not-found", "Directory does not exist: Nowhere", "report")

    def test_clean_a_relative_path_or_none_from_a_working_directory_that_is_gone(self):
        # pcl:449-451: a relative path, or no argument, is made absolute against
        # the working directory and refused target-not-repository-root where Git
        # finds no worktree there; with the working directory gone Git finds
        # none, and the refusal names the argument as given, or `.` (lane 3's
        # US7/US9 L-3, which ended in internal-error).
        for words, shown in (((), "."), ((".",), "."), (("./sub",), "./sub")):
            with self.subTest(words=words):
                argv = ("clean", *words, "--json")
                result = self.document_of(*self.main_in_a_gone_directory(*argv), argv)
                self.assert_error_document(result, "target-not-repository-root", self.not_root(shown), "report",
                                           path=shown)
                status, out, err = self.main_in_a_gone_directory("clean", *words)
                self.assertEqual((status, out, err), (2, "", f"REFUSED: {self.not_root(shown)}\n"))

    def test_clean_a_relative_path_s_refusal_names_the_directory_git_examined(self):
        # Lane 3's US7/US9 L-2, wording only: `ln-inner/..` from `work`, where
        # ln-inner is a symbolic link to ../other/dir/inner, examines other/dir
        # (chdir() takes `..` after the link), so the refusal names other/dir,
        # not work, the lexical result.
        work = self.base / "work"
        inner = self.base / "other" / "dir" / "inner"
        work.mkdir()
        inner.mkdir(parents=True)
        (work / "ln-inner").symlink_to(Path("..") / "other" / "dir" / "inner")
        examined = self.base / "other" / "dir"
        result = self.run_json("clean", "ln-inner/..", "--json", cwd=work)
        self.assert_error_document(result, "target-not-repository-root", self.not_root(examined), "report",
                                   path=examined)
        self.assert_refused_human(self.run_cli("clean", "ln-inner/..", cwd=work), self.not_root(examined))

    # R-71 (b): row 3 runs once, where the argument resolves.

    def test_clean_row_3_runs_once_where_the_argument_resolves(self):
        root = self.repo()
        self.bare_remote()
        linked = self.merged_worktree("001-merged")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        runs = (("an absolute path", ("clean", root, "--all-safe", "--json"), self.base, [], [str(root)]),
                ("a relative path in a linked worktree", ("clean", "--all-safe", "--json"), linked, [],
                 [str(linked), str(root)]),
                ("a relative path in a linked worktree, `.`", ("clean", ".", "--json"), linked, [],
                 [os.path.join(str(linked), "."), str(root)]),  # joined to the working directory as given
                ("a bare name", ("clean", "repo", "--all-safe", "--json"), elsewhere, [str(root)], [str(root)]))
        for label, words, cwd, row_2, row_3 in runs:
            with self.subTest(label):
                result, records = self.counted(*words, cwd=cwd)
                self.assert_status(result, 0)
                self.assertEqual(result.document["repository"], self.repository(root))
                self.assertEqual(result.document["root"], str(root))
                commands = [command(record) for record in records]
                self.assertEqual([c[1] for c in commands if c[2:] == ROW_2], row_2, "row 2: the name lookup")
                self.assertEqual([c[1] for c in commands if c[2:] == ROW_3], row_3,
                                 "row 3 once where the argument resolves, then row 5 at root only from elsewhere")
                self.assertEqual(sorted(c[1] for c in commands if c[2:] == STATUS), sorted([str(root), str(linked)]))

    # Plan review F2: row 5 failing.

    def test_clean_row_5_failing_still_resolves_to_the_main_worktree(self):
        # pcl "Clean resolves its target Git-first": a relative path, or no
        # argument, resolves to the repository Git finds "with `root` set to
        # its main worktree", and an absolute path must be the main worktree.
        # Row 5, row 3 again at the main worktree, fails here (a fake git fails
        # `-C ROOT rev-parse`); lead ruling R-73 (e)(1) keeps the plan
        # incomplete rather than refused, and its root is still the main
        # worktree, never the linked worktree the command ran in.
        root = self.repo()
        self.bare_remote()
        linked = self.merged_worktree("001-merged")
        fake = self.base / "fake-row-5" / "git"
        fake.parent.mkdir()
        fake.write_text("#!/bin/sh\np2=; p1=\nfor a in \"$@\"; do\n"
                        f"  if [ \"x$p2\" = x-C ] && [ \"x$p1\" = x{shlex.quote(str(root))} ] && "
                        "[ \"x$a\" = xrev-parse ]; then\n"
                        "    echo 'fatal: row 5 failed (fake)' >&2; exit 128\n  fi\n  p2=$p1; p1=$a\ndone\n"
                        f"exec {shlex.quote(clean_support.REAL_GIT)} \"$@\"\n")
        fake.chmod(0o755)
        env = self.path_first(fake.parent)
        for words in ((), (".",)):
            with self.subTest(words=words):
                result = self.run_json("clean", *words, "--json", cwd=linked, env=env)
                self.assert_status(result, 1)
                self.assertEqual((result.document["root"], result.document["completeness"]),
                                 (str(root), "incomplete"))
        with self.subTest("an absolute path to the linked worktree is still refused"):
            result = self.run_json("clean", linked, "--json", env=env)
            self.assert_error_document(result, "target-not-repository-root", self.not_root(linked), "report",
                                       path=linked)

    # T105: "A bare repository reached from a linked worktree".

    def test_clean_a_bare_repository_reached_from_a_linked_worktree(self):
        seed = self.repo("seed")
        bare = self.base / "bare.git"
        self.git(self.base, "init", "-q", "--bare", bare)
        self.git(seed, "push", "-q", bare, "main")
        linked = self.base / "linked"
        self.git(bare, "worktree", "add", "-q", linked, "main")
        before = self.snapshot(bare)
        message = self.not_root(linked)
        for words in ((), (".",), ("./",), ("--all-safe", "--apply", "--yes")):
            with self.subTest(words=words):
                result, records = self.counted("clean", *words, cwd=linked)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                result, records = self.counted("clean", *words, "--json", cwd=linked)
                mode = "all-safe" if "--all-safe" in words else "report"
                self.assert_error_document(result, "target-not-repository-root", message, mode, path=linked)
        with self.subTest("a bare name inside one of its linked worktrees"):
            result = self.run_cli("clean", "linked", "--all-safe", cwd=linked)
            self.assert_refused_human(result, message)
        self.assertEqual(self.snapshot(bare), before, "nothing changes")

    # T105: "A separate git directory".

    def test_clean_a_separate_git_directory(self):
        checkout, gitdir = self.base / "checkout", self.base / "checkout.git"
        self.git(self.base, "init", "-q", "-b", "main", "--separate-git-dir", gitdir, checkout)
        self.git(checkout, "commit", "-q", "--allow-empty", "-m", "initial")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        for words in (("--json",), ("--all-safe", "--json")):
            with self.subTest(words=words):
                document = self.run_json("clean", checkout, *words, cwd=elsewhere).document
                self.assertEqual(document["repository"], self.repository(checkout, gitdir))
                self.assertEqual(document["root"], str(checkout))
                self.assertEqual([row["path"] for row in document["worktrees"]], [str(checkout)],
                                 "the git directory is no worktree row")

    def test_clean_a_separate_git_directory_with_a_relative_core_worktree(self):
        # Lead ruling R-36: a relative core.worktree resolves against the git
        # directory, as Git documents and project-overview's spec states.
        checkout, gitdir = self.base / "checkout", self.base / "checkout.git"
        self.git(self.base, "init", "-q", "-b", "main", "--separate-git-dir", gitdir, checkout)
        self.git(checkout, "commit", "-q", "--allow-empty", "-m", "initial")
        self.git(checkout, "config", "core.worktree", "../checkout")
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        result, records = self.counted("clean", checkout, "--json", cwd=elsewhere)
        self.assert_status(result, 0)
        self.assertEqual(result.document["repository"], self.repository(os.path.realpath(checkout), gitdir))
        self.assertEqual([row["path"] for row in result.document["worktrees"]], [str(checkout)])
        self.assertIn(["config", "--get", "core.worktree"], [command(record)[2:] for record in records],
                      "row 4b named the main worktree")

    # T105: "A submodule checkout".

    def test_clean_a_submodule_checkout(self):
        superproject = self.repo("super")
        submodule = self.submodule(superproject)
        self.commit(superproject)
        before = self.snapshot(superproject)
        message = self.not_root(submodule)
        for words, cwd, path in (((submodule,), self.base, submodule), ((), submodule, submodule),
                                 ((submodule, "--all-safe", "--apply", "--yes"), self.base, submodule)):
            with self.subTest(words=words, cwd=cwd):
                result, records = self.counted("clean", *words, cwd=cwd)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                result, records = self.counted("clean", *words, "--json", cwd=cwd)
                mode = "all-safe" if "--all-safe" in words else "report"
                self.assert_error_document(result, "target-not-repository-root", message, mode, path=path)
        self.assertEqual(self.snapshot(superproject), before, "nothing changes")

    # #19's round (i) (design.md D6 and D18 at e0c91bb; lead ruling R-271): a
    # main worktree that a core.worktree or core.bare of the repository's own
    # redirects is refused target-not-repository-root, as before, but with the
    # variant that names the redirect; every other such refusal keeps the
    # plain message.

    def redirected(self, path):
        return TEXT["target_not_repository_root_redirect"].format(PATH=path)

    def row_3b_dirs(self, records):
        return [command(record)[1] for record in records if command(record)[2:] == ROW_3B]

    def redirect(self, root, key, value, place):
        """Inline fixture (rule 3): set key to value for root's main worktree in
        place, "config" (the repository's own) or "config.worktree" (the main
        worktree's, with extensions.worktreeConfig set true), through the real
        git's `config --file`. Returns the git directory."""
        gitdir = Path(self.git(root, "rev-parse", "--path-format=absolute", "--git-dir").rstrip("\n"))
        if place == "config.worktree":
            self.git(root, "config", "extensions.worktreeConfig", "true")
        self.git(root, "config", "--file", gitdir / place, key, value)
        return gitdir

    def unset_redirect(self, gitdir):
        """What the variant says: unset core.worktree and core.bare in the git
        directory's config and config.worktree."""
        for place in ("config", "config.worktree"):
            if (gitdir / place).exists():
                for key in ("core.worktree", "core.bare"):
                    self.git(self.base, "config", "--file", gitdir / place, "--unset", key, check=False)

    def test_clean_a_redirected_main_worktree_names_the_redirect(self):
        # D18: a core.bare true, or a core.worktree naming another directory (a
        # missing one included), in the repository's config or in the main
        # worktree's config.worktree, is refused target-not-repository-root,
        # exit 2, before any plan, with the variant. Row 3b runs once, in the
        # root, only where row 3 failed (core.bare); once both settings are
        # unset, as the variant says, the root resolves, and that run spawns no
        # row 3b. Identical on Git 2.43.0 and 2.36.6 (round (i)'s fixtures).
        cases = (("core.bare true in the repository's config", "core.bare", None, "config"),
                 ("core.worktree naming another directory in the repository's config",
                  "core.worktree", "other", "config"),
                 ("core.bare true in the main worktree's config.worktree", "core.bare", None, "config.worktree"),
                 ("core.worktree naming another directory in the main worktree's config.worktree",
                  "core.worktree", "other", "config.worktree"),
                 ("core.worktree naming a missing directory", "core.worktree", "missing", "config"))
        modes = (("report", ()), ("all-safe", ("--all-safe", "--apply", "--yes")))
        for number, (label, key, target, place) in enumerate(cases):
            with self.subTest(label):
                root = self.repo(f"redirected-{number}")
                value = "true"
                if key == "core.worktree":
                    value = str(self.base / f"{target}-{number}")
                    if target == "other":
                        Path(value).mkdir()
                gitdir = self.redirect(root, key, value, place)
                message = self.redirected(root)
                row_3b = [str(root)] if key == "core.bare" else []
                for mode, words in modes:
                    result, records = self.counted("clean", root, *words)
                    self.assert_refused_human(result, message)
                    self.assert_no_plan(records)
                    self.assertEqual(self.row_3b_dirs(records), row_3b, "row 3b only where row 3 failed")
                    result, records = self.counted("clean", root, *words, "--json")
                    self.assert_error_document(result, "target-not-repository-root", message, mode, path=root)
                    self.assert_no_plan(records)
                result, records = self.counted("clean", root, "--apply", "--action", "delete-branch",
                                               "--branch", "main", "--yes")
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                if key == "core.bare":  # no argument, from the root itself: Git finds no worktree there
                    result, records = self.counted("clean", cwd=root)
                    self.assert_refused_human(result, message)
                    self.assertEqual(self.row_3b_dirs(records), row_3b)
                self.unset_redirect(gitdir)
                result, records = self.counted("clean", root, "--json")
                self.assert_status(result, 0)
                self.assertEqual(result.document["root"], str(root))
                self.assertEqual(self.row_3b_dirs(records), [], "a run that resolves spawns no row 3b")

    def test_clean_a_redirected_main_worktree_whose_git_is_a_file(self):
        # D18 with D8's gitfile layout (`git init --separate-git-dir`): a
        # core.worktree naming another directory, or a core.bare true, takes
        # the variant, row 3b running only for the core.bare, and with both
        # unset the checkout resolves; a core.worktree naming the checkout
        # itself resolves as before (D8), with no row 3b.
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        other = self.base / "other"
        other.mkdir()
        cases = (("core.worktree naming another directory", "core.worktree", str(other), True),
                 ("core.bare true", "core.bare", "true", True),
                 ("core.worktree naming the checkout itself", "core.worktree", None, False))
        for number, (label, key, value, refused) in enumerate(cases):
            with self.subTest(label):
                checkout, gitdir = self.base / f"checkout-{number}", self.base / f"checkout-{number}.git"
                self.git(self.base, "init", "-q", "-b", "main", "--separate-git-dir", gitdir, checkout)
                self.git(checkout, "commit", "-q", "--allow-empty", "-m", "initial")
                self.git(checkout, "config", key, str(checkout) if value is None else value)
                result, records = self.counted("clean", checkout, "--json", cwd=elsewhere)
                if refused:
                    self.assert_error_document(result, "target-not-repository-root", self.redirected(checkout),
                                               "report", path=checkout)
                    self.assert_no_plan(records)
                    self.assertEqual(self.row_3b_dirs(records), [str(checkout)] if key == "core.bare" else [])
                    self.assert_refused_human(self.run_cli("clean", checkout, cwd=elsewhere),
                                              self.redirected(checkout))
                    self.unset_redirect(gitdir)
                    result, records = self.counted("clean", checkout, "--json", cwd=elsewhere)
                self.assert_status(result, 0)
                self.assertEqual(result.document["root"], str(checkout))
                self.assertEqual(self.row_3b_dirs(records), [], "a run that resolves spawns no row 3b")

    def test_clean_a_bare_repository_beside_a_main_worktree_that_core_bare_redirects(self):
        # D18: a `git init --bare` repository passed by its own directory holds
        # no .git, keeps the plain message and runs no row 3b, and an unset of
        # its core.bare does not make it a work tree. One made by `git init
        # --bare X/.git` and passed as X has the configuration of a checkout at
        # X whose core.bare is true, which nothing Git reads tells apart, so it
        # takes the variant, which is true of it: with core.bare unset X
        # resolves.
        seed = self.repo("seed")
        bare = self.base / "plain.git"
        self.git(self.base, "init", "-q", "--bare", bare)
        self.git(seed, "push", "-q", bare, "main")
        holder = self.base / "holder"
        holder.mkdir()
        self.git(self.base, "init", "-q", "--bare", holder / ".git")
        self.git(seed, "push", "-q", holder / ".git", "main")
        for label, path, message, row_3b in (
                ("passed by its own directory", bare, self.not_root(bare), []),
                ("made at X/.git and passed as X", holder, self.redirected(holder), [str(holder)])):
            with self.subTest(label):
                result, records = self.counted("clean", path)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                self.assertEqual(self.row_3b_dirs(records), row_3b)
                result, records = self.counted("clean", path, "--all-safe", "--json")
                self.assert_error_document(result, "target-not-repository-root", message, "all-safe", path=path)
        with self.subTest("core.bare unset"):
            self.git(self.base, "config", "--file", bare / "config", "--unset", "core.bare")
            self.assert_refused_human(self.run_cli("clean", bare), self.not_root(bare))
            self.git(self.base, "config", "--file", holder / ".git" / "config", "--unset", "core.bare")
            document = self.run_json("clean", holder, "--json").document
            self.assertEqual(document["root"], str(holder))

    def test_clean_plain_refusals_beside_a_redirected_main_worktree(self):
        # D18: only the directory where the main worktree would be takes the
        # variant. Beside a root whose own config sets core.bare true, its
        # subdirectory and its linked worktree keep the plain message, by an
        # absolute path and with no argument from inside them, and so do a
        # linked worktree that its own config.worktree redirects, by core.bare
        # (row 3 fails there, and row 3b runs and finds that worktree's git
        # directory, not the common one) or by core.worktree (its .git names
        # no common directory, and no row 3b runs), a submodule checkout and a
        # directory outside any repository.
        root = self.repo()
        linked = self.base / "linked"
        self.git(root, "worktree", "add", "-q", "-b", "linked", linked)
        (root / "sub").mkdir()
        self.git(root, "config", "core.bare", "true")
        other = self.repo("other")
        redirected = self.base / "other-linked"
        self.git(other, "worktree", "add", "-q", "-b", "other-linked", redirected)
        decoyed = self.base / "other-decoyed"
        self.git(other, "worktree", "add", "-q", "-b", "other-decoyed", decoyed)
        decoy = self.base / "decoy"
        decoy.mkdir()
        self.git(other, "config", "extensions.worktreeConfig", "true")
        self.git(redirected, "config", "--worktree", "core.bare", "true")
        self.git(decoyed, "config", "--worktree", "core.worktree", decoy)
        superproject = self.repo("super")
        submodule = self.submodule(superproject)
        self.commit(superproject)
        outside = self.base / "outside"
        outside.mkdir()
        cases = (("the redirected root", root, self.redirected(root), [str(root)]),
                 ("its subdirectory", root / "sub", self.not_root(root / "sub"), []),
                 ("its linked worktree", linked, self.not_root(linked), []),
                 ("a linked worktree that its own config.worktree makes bare", redirected,
                  self.not_root(redirected), [str(redirected)]),
                 ("a linked worktree that its own config.worktree sends elsewhere", decoyed,
                  self.not_root(decoyed), []),
                 ("a submodule checkout", submodule, self.not_root(submodule), []),
                 ("a directory outside any repository", outside, self.not_root(outside), []))
        for label, path, message, row_3b in cases:
            with self.subTest(label):
                result, records = self.counted("clean", path)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                self.assertEqual(self.row_3b_dirs(records), row_3b)
                result, records = self.counted("clean", path, "--all-safe", "--json")
                self.assert_error_document(result, "target-not-repository-root", message, "all-safe", path=path)
        for path in (linked, root / "sub"):
            with self.subTest("no argument", cwd=path):
                self.assert_refused_human(self.run_cli("clean", cwd=path), self.not_root(path))

    def test_clean_a_row_3b_that_fails_or_is_cut_keeps_the_plain_message(self):
        # D6 and D18: row 3b is one `probe` child through run_bounded(), counted
        # and bounded as row 3 is, run once and only on the refusal; one that
        # fails, times out or meets the work deadline leaves the plain message.
        root = self.repo()
        self.git(root, "config", "core.bare", "true")
        real = project.run_bounded
        for name, exit_status in (("failed", 128), ("timeout", None), ("deadline", None)):
            attempts = []

            def stand_in(spec, parser, run, name=name, exit_status=exit_status, attempts=attempts):
                kind, args, cwd = spec
                if "--is-bare-repository" in args:
                    attempts.append((kind, [os.fsdecode(arg) for arg in args]))
                    return project.DriverOutcome(project.git_argv(kind, args), name, status=exit_status,
                                                 detail="stand-in")
                return real(spec, parser, run)

            with self.subTest(outcome=name):
                status, out, err = self.main_in_process("clean", root, run_bounded=stand_in)
                self.assertEqual((status, out, err), (2, "", f"REFUSED: {self.not_root(root)}\n"))
                self.assertEqual(attempts, [("probe", ["-C", str(root), *ROW_3B])])
        with self.subTest("the same run, row 3b answering, takes the variant"):
            status, out, err = self.main_in_process("clean", root)
            self.assertEqual((status, out, err), (2, "", f"REFUSED: {self.redirected(root)}\n"))

    # T106: "Merge target missing, invalid, or conflicting".

    def test_clean_merge_target_missing_invalid_or_conflicting(self):
        with self.subTest("no candidate"):
            root = self.repo("none", branch="trunk")
            message = TEXT["no_merge_target"]
            before = self.snapshot(root)
            for words, mode in (((), "report"), (("--all-safe", "--apply", "--yes"), "all-safe")):
                result, records = self.counted("clean", root, *words)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                result, records = self.counted("clean", root, *words, "--json")
                self.assert_error_document(result, "no-merge-target", message, mode, repository=self.repository(root))
                self.assert_no_plan(records)
            self.assertEqual(self.snapshot(root), before)
        with self.subTest("a manifest of the wrong kind"):
            root = self.repo("wrong-kind")
            (root / "project.yaml").write_text("kind: family-manifest\n")
            message = f"Unexpected kind in {root / 'project.yaml'}; expected project-manifest"
            result, records = self.counted("clean", root)
            self.assert_refused_human(result, message)
            self.assert_no_plan(records)
            result, records = self.counted("clean", root, "--all-safe", "--json")
            self.assert_error_document(result, "manifest-invalid", message, "all-safe",
                                       repository=self.repository(root))
            self.assert_no_plan(records)
        with self.subTest("the manifest names release, origin/HEAD names main"):
            root = self.repo("conflict")
            self.bare_remote(root=root, name="conflict-remote.git")
            (root / "project.yaml").write_text("kind: project-manifest\ntracking_branch: release\n")
            self.commit(root)
            self.git(root, "push", "-q", "-u", "origin", "main")
            self.git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
            release = self.git(root, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "release").strip()
            self.git(root, "update-ref", "refs/heads/release", release)
            document = self.run_json("clean", root, "--all-safe", "--json").document
            self.assertEqual(document["merge_target"], {"name": "release", "source": "manifest", "sha": release})
            self.assertEqual(document["notes"], [{"code": "merge-target-conflict", "message": TEXT[
                "note_merge_target_conflict"].format(NAME="release", OTHER="main")}])
            self.assertEqual((document["completeness"], document["apply_allowed"]), ("complete", True))
            result = self.run_cli("clean", root, "--all-safe")
            self.assert_status(result, 0)
            self.assertIn(TEXT["merge_target_line"].format(NAME="release", SOURCE="manifest"),
                          result.stdout.splitlines())
        with self.subTest("no manifest candidate, origin/HEAD names trunk"):
            root = self.repo("origin-head")
            self.bare_remote(root=root, name="origin-head-remote.git")
            trunk = self.git(root, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "trunk").strip()
            self.git(root, "update-ref", "refs/heads/trunk", trunk)
            self.git(root, "push", "-q", "origin", "trunk")
            self.git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/trunk")
            for words in (("--json",), ("--all-safe", "--json")):
                document = self.run_json("clean", root, *words).document
                self.assertEqual(document["merge_target"], {"name": "trunk", "source": "origin-head", "sha": trunk})
                self.assertEqual((document["target_branch"], document["notes"]), ("trunk", []))

    def test_clean_merge_target_missing_invalid_or_conflicting_unreadable_manifest(self):
        # T108: an unreadable file, a parse error, a value that is not a mapping
        # and a wrong kind each refuse manifest-invalid with manifest()'s and
        # read_yaml()'s baseline messages; family.yaml when there is no
        # project.yaml file, as manifest() picks it.
        root = self.repo()
        manifest = root / "project.yaml"
        family = root / "family.yaml"
        cases = (
            ("a parse error", manifest, "kind: [unclosed\n", f"Cannot read {manifest}: "),
            ("not a mapping", manifest, "- kind\n- project-manifest\n", f"Expected a mapping in {manifest}"),
            ("family.yaml of the wrong kind", family, "kind: project-manifest\n",
             f"Unexpected kind in {family}; expected family-manifest"),
        )
        for label, path, text, message in cases:
            with self.subTest(label):
                path.write_text(text)
                result = self.run_json("clean", root, "--json")
                self.assert_status(result, 2)
                document = result.document
                self.assertEqual((document["code"], document["repository"]), ("manifest-invalid", self.repository(root)))
                if message.endswith(": "):
                    self.assertTrue(document["error"].startswith(message), document["error"])
                    self.assertGreater(len(document["error"]), len(message))
                else:
                    self.assertEqual(document["error"], message)
                path.unlink()
        with self.subTest("a directory named project.yaml is no manifest"):
            manifest.mkdir()
            family.write_text("kind: family-manifest\ntracking_branch: main\n")
            document = self.run_json("clean", root, "--json").document
            self.assertEqual(document["merge_target"]["source"], "manifest")
            family.unlink()
            manifest.rmdir()
        with self.subTest("an unreadable file"):
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                self.skipTest("permission fixtures do not bind the superuser (effective uid 0)")
            manifest.write_text("kind: project-manifest\n")
            manifest.chmod(0)
            self.addCleanup(manifest.chmod, 0o644)
            result = self.run_json("clean", root, "--json")
            message = f"Cannot read {manifest}: [Errno 13] Permission denied: '{manifest}'"
            self.assert_error_document(result, "manifest-invalid", message, "report", repository=self.repository(root))

    def test_clean_merge_target_missing_invalid_or_conflicting_a_value_pyyaml_cannot_build(self):
        # Lane 3's US7/US9 M-1, lead ruling R-101 (e): "a manifest that cannot
        # be read ... SHALL refuse with manifest-invalid". PyYAML raises
        # ValueError, KeyError, AttributeError or RecursionError, not a
        # YAMLError, for these values; each is a manifest that does not parse,
        # where c9103ba ended in internal-error.
        root = self.repo()
        manifest = root / "project.yaml"
        cases = (
            ("an impossible date", "released: 2021-02-30\n"),
            ("an unknown boolean", "flag: !!bool maybe\n"),
            ("a malformed timestamp", "when: !!timestamp soon\n"),
            ("nesting past the recursion limit", "deep: " + "[" * 100000 + "\n"),
        )
        for label, text in cases:
            with self.subTest(label):
                manifest.write_text("kind: project-manifest\n" + text)
                result, records = self.counted("clean", root, "--json")
                self.assert_status(result, 2)
                document = result.document
                self.assertEqual((document["code"], document["repository"]),
                                 ("manifest-invalid", self.repository(root)))
                self.assertTrue(document["error"].startswith(f"Cannot read {manifest}: "), document["error"])
                self.assert_no_plan(records)
                result = self.run_cli("clean", root, "--all-safe")
                self.assert_status(result, 2)
                self.assertTrue(result.stderr.startswith(f"REFUSED: Cannot read {manifest}: "), result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    # T106: "A tracking branch spelled with its remote".

    def test_clean_a_tracking_branch_spelled_with_its_remote(self):
        root = self.repo()
        self.bare_remote()
        (root / "project.yaml").write_text("kind: project-manifest\ntracking_branch: origin/develop\n")
        self.commit(root)
        self.git(root, "push", "-q", "-u", "origin", "main")
        self.git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        published = self.git(root, "commit-tree", "HEAD^{tree}", "-p", "HEAD", "-m", "develop").strip()
        self.git(root, "update-ref", "refs/heads/develop", published)
        self.git(root, "push", "-q", "origin", "develop")
        local = self.git(root, "commit-tree", "HEAD^{tree}", "-p", published, "-m", "local").strip()
        self.git(root, "update-ref", "refs/heads/develop", local)
        self.assertNotEqual(self.git(root, "rev-parse", "refs/remotes/origin/develop").strip(), local)
        for words in (("--json",), ("--all-safe", "--json")):
            with self.subTest(words=words):
                document = self.run_json("clean", root, *words).document
                self.assertEqual(document["merge_target"], {"name": "develop", "source": "manifest", "sha": local},
                                 "read from refs/heads/develop, never main by a silent fallback")
                self.assertEqual(document["notes"], [{"code": "merge-target-conflict", "message": TEXT[
                    "note_merge_target_conflict"].format(NAME="develop", OTHER="main")}])

    def test_clean_resolve_merge_target_notes_a_conflict(self):
        # T108, R-56 (P-13): the note only when the manifest's candidate and the
        # origin/HEAD one both exist as local branches and differ.
        def ref(name, symref=b""):
            return {"refname": name, "objectname": name.decode()[-1] * 40, "symref": symref}
        head = ref(b"refs/remotes/origin/HEAD", b"refs/remotes/origin/main")
        branches = [ref(b"refs/heads/main"), ref(b"refs/heads/release"), head]
        note = {"code": "merge-target-conflict",
                "message": TEXT["note_merge_target_conflict"].format(NAME="release", OTHER="main")}
        for declared, refs, expected in (
                ("release", branches, ("release", "manifest", [note])),
                ("origin/release", branches, ("release", "manifest", [note])),
                ("origin/main", branches, ("main", "manifest", [])),
                ("gone", branches, ("main", "origin-head", [])),
                (None, branches, ("main", "origin-head", [])),
                ("release", [ref(b"refs/heads/main"), ref(b"refs/heads/release"),
                             ref(b"refs/remotes/origin/HEAD", b"refs/remotes/origin/feature")],
                 ("release", "manifest", []))):
            with self.subTest(declared=declared):
                target = project.resolve_merge_target(refs, declared)
                self.assertEqual((target["name"], target["source"], target["notes"]), expected)
        trunk_only = [ref(b"refs/heads/trunk")]
        with self.assertRaises(project.Refused) as caught:
            project.resolve_merge_target(trunk_only, None)
        self.assertEqual((str(caught.exception), caught.exception.code), (TEXT["no_merge_target"], "no-merge-target"))

    # T106: "A manifest over 1 MiB".

    def test_clean_a_manifest_over_1_mib(self):
        root = self.repo()
        self.bare_remote()
        self.merged_worktree("001-merged")
        manifest = root / "project.yaml"
        manifest.write_text(manifest_text(MIB + 1, "kind: project-manifest", "tracking_branch: main"))
        message = TEXT["manifest_invalid_size"].format(PATH=manifest)
        before = self.snapshot(root)
        for words, mode in (((), "report"), (("--all-safe",), "all-safe"), (("--all-safe", "--apply", "--yes"),
                                                                             "all-safe")):
            with self.subTest(words=words):
                result, records = self.counted("clean", root, *words)
                self.assert_refused_human(result, message)
                self.assert_no_plan(records)
                result, records = self.counted("clean", root, *words, "--json")
                self.assert_error_document(result, "manifest-invalid", message, mode, repository=self.repository(root))
                self.assertEqual([record for record in records if command(record)[2:3] == ["status"]], [],
                                 "no status child: no worktree row is probed")
        self.assertEqual(self.snapshot(root), before)

        opened = []
        real_open = builtins.open

        class Recorded:
            """The file opened, each read's requested size recorded."""

            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                self.stream.close()

            def fileno(self):
                return self.stream.fileno()

            def read(self, size=-1):
                opened.append(("read", size))
                return self.stream.read(size)

        def recording_open(path, *args, **kwargs):
            if os.fsdecode(path).endswith("project.yaml"):
                opened.append(("open", os.fsdecode(path)))
                return Recorded(real_open(path, *args, **kwargs))
            return real_open(path, *args, **kwargs)

        def read_yaml(path):
            opened.append(("read_yaml", str(path)))
            raise AssertionError("read_yaml() is never reached for the manifest")

        with self.subTest("in process: the file is never read"):
            status, out, err = self.main_in_process("clean", root, "--json", read_yaml=read_yaml,
                                                    open=recording_open)
            self.assertEqual((status, err, json.loads(out)["code"]), (2, "", "manifest-invalid"))
            self.assertEqual(opened, [])
        with self.subTest("exactly 1 MiB is read, at most 1 MiB asked"):
            manifest.write_text(manifest_text(MIB, "kind: project-manifest", "tracking_branch: main"))
            status, out, err = self.main_in_process("clean", root, "--json", read_yaml=read_yaml,
                                                    open=recording_open)
            self.assertEqual((status, err), (0, ""), out)
            self.assertEqual(json.loads(out)["merge_target"]["source"], "manifest")
            self.assertEqual([entry[0] for entry in opened], ["open", "read"])
            self.assertTrue(all(0 <= size <= MIB for kind, size in opened if kind == "read"), opened)

    # Brett Heap's ruling LQ-15 (lead ruling R-102): "A relative configuration path".

    def plant_configuration(self, root, config):
        """Inline fixture (rule 3): commit in root, at the relative path config, a
        configuration whose clean filter `mark`, which root's tracked
        .gitattributes selects for *.txt, and whose core.hooksPath, root's
        tracked hooks/, each append to self.base/marker, beside a tracked
        data.txt. The fixture's own git reads none of it (GIT_CONFIG_GLOBAL is
        os.devnull). Returns the marker's path."""
        marker = self.base / "marker"
        quoted = shlex.quote(str(marker))
        hooks = root / "hooks"
        hooks.mkdir()
        for name in ("pre-push", "reference-transaction", "post-checkout", "post-merge"):
            (hooks / name).write_text(f"#!/bin/sh\necho {name} >> {quoted}\n")
            (hooks / name).chmod(0o755)
        path = root / config
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'[filter "mark"]\n\tclean = "tee -a {quoted}"\n[core]\n\thooksPath = "{hooks}"\n')
        (root / ".gitattributes").write_text("*.txt filter=mark\n")
        (root / "data.txt").write_text("data\n")
        self.commit(root)
        return marker

    def stale_stat(self, path):
        """Move path's mtime an hour back, so that its index entry no longer
        matches and a status probe reads the file through its clean filter."""
        found = os.stat(path)
        os.utime(path, (found.st_atime - 3600, found.st_mtime - 3600))

    def assert_planted_configuration_is_live(self, root, marker, env):
        """The control: the real git, run in root under env with no optional
        lock, reads the planted file as the user's configuration, and its
        filter writes the marker, which is then removed."""
        self.assertFalse(marker.exists())
        self.git(root, "status", "--porcelain", env=dict(env, GIT_OPTIONAL_LOCKS="0"))
        self.assertTrue(marker.exists(), "the planted filter runs under the real git: the fixture is live")
        marker.unlink()

    def test_clean_a_relative_configuration_path(self):
        # D11's test runs after the argument checks and before the version
        # check, so a relative HOME refuses the read-only form, the batch apply
        # and the push with exit 2 and starts no Git child, git --version
        # included. The control shows the real git reading h/.gitconfig under
        # the same environment. Beside an absolute XDG_CONFIG_HOME and an
        # absolute GIT_CONFIG_GLOBAL, Git would read nothing under HOME, and
        # the test still refuses (it does not follow Git's precedence).
        root = self.repo()
        marker = self.plant_configuration(root, "h/.gitconfig")
        self.bare_remote()
        self.merged_worktree("001-merged")
        self.stale_stat(root / "data.txt")
        before = self.snapshot(root)
        live = {name: value for name, value in self.env.items() if name != "GIT_CONFIG_GLOBAL"}
        live["HOME"] = "h"
        beside = dict(self.env, HOME="h", XDG_CONFIG_HOME=str(self.base / "xdg"))  # GIT_CONFIG_GLOBAL os.devnull
        message = config_lines("HOME")
        modes = (("read-only", ()), ("all-safe apply", ("--all-safe", "--apply", "--yes")),
                 ("push", ("--apply", "--action", "push", "--branch", "001-merged", "--yes")))
        for label, env in (("Git would read h/.gitconfig", live),
                           ("beside an absolute XDG_CONFIG_HOME and GIT_CONFIG_GLOBAL", beside)):
            if env is live:
                self.assert_planted_configuration_is_live(root, marker, env)
            for mode, words in modes:
                with self.subTest(label, mode=mode):
                    result, records = self.counted("clean", root, *words, env=env)
                    self.assert_refused_human(result, message)
                    self.assertEqual(records, [], "no Git child, git --version included")
            with self.subTest(label, mode="read-only", output="json"):
                result, records = self.counted("clean", root, "--json", env=env)
                self.assert_error_document(result, "relative-config-path", message, "report")
                self.assertEqual(records, [])
        self.assertFalse(marker.exists(), "no filter or hook ran")
        self.assertEqual(self.snapshot(root), before, "nothing changes")

    def test_clean_a_relative_configuration_path_each_variable_and_spelling(self):
        # The scenario's other ANDs: a relative XDG_CONFIG_HOME beside an
        # absolute HOME; a HOME of " /x", "~/x" or "."; a relative
        # GIT_CONFIG_GLOBAL or GIT_CONFIG_SYSTEM beside an absolute HOME (the
        # lead's extension). Every variable that fails is named, one line each,
        # in D18's order, and no value is printed.
        root = self.repo()
        cases = [({"XDG_CONFIG_HOME": "cfg"}, ("XDG_CONFIG_HOME",)),
                 ({"HOME": " /x"}, ("HOME",)), ({"HOME": "~/x"}, ("HOME",)), ({"HOME": "."}, ("HOME",)),
                 # Lead ruling R-202 (lane 3's W30 M-2): the commonest relative spelling.
                 ({"HOME": "./h"}, ("HOME",)), ({"XDG_CONFIG_HOME": "./cfg"}, ("XDG_CONFIG_HOME",))]
        cases += [({name: "h/.gitconfig"}, (name,)) for name in EXTENSION]
        cases.append(({"HOME": "h", "XDG_CONFIG_HOME": "cfg", **{name: "h/.gitconfig" for name in EXTENSION}},
                      ("HOME", "XDG_CONFIG_HOME", *EXTENSION)))
        for values, names in cases:
            env = dict(self.env, **values)
            with self.subTest(values=values):
                result, records = self.counted("clean", root, "--all-safe", env=env)
                self.assert_refused_human(result, config_lines(*names))
                self.assertEqual(records, [])
                for value in values.values():
                    if len(value) > 1:  # "." and "h" are letters of the message itself
                        self.assertNotIn(value, result.stderr, "the value is never printed")
            with self.subTest(values=values, output="json"):
                result, records = self.counted("clean", root, "--all-safe", "--json", env=env)
                self.assert_error_document(result, "relative-config-path", config_lines(*names), "all-safe")
                self.assertEqual(records, [])

    def test_clean_a_relative_configuration_path_not_valid_utf_8(self):
        # D11: the test is made on the raw bytes, so a relative value whose
        # first byte is not UTF-8 fails it too; the message names the variable.
        root = self.repo()
        for name in ("HOME", "XDG_CONFIG_HOME", *EXTENSION):
            env = dict(self.env)
            env[name] = b"\xffh"
            with self.subTest(name=name):
                result, records = self.counted("clean", root, env=env)
                self.assert_refused_human(result, config_lines(name))
                self.assertEqual(records, [])
                result, records = self.counted("clean", root, "--json", env=env)
                self.assert_error_document(result, "relative-config-path", config_lines(name), "report")
                self.assertEqual(records, [])

    def test_clean_a_relative_configuration_path_empty_and_absolute_values_pass(self):
        # The scenario's last AND: with HOME absolute, XDG_CONFIG_HOME empty,
        # and GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM unset, clean is not
        # refused for them. Nor is it for an empty value, `/` alone, or an
        # absolute value that is not UTF-8; beside one relative variable, such
        # a value is not named, and the run goes on to the version check.
        root = self.repo()
        unset = {name: value for name, value in self.env.items() if name not in EXTENSION}
        with self.subTest("HOME absolute, XDG_CONFIG_HOME empty, the two unset"):
            result, records = self.counted("clean", root, "--json", env=dict(unset, XDG_CONFIG_HOME=""))
            self.assert_status(result, 0)
            self.assertEqual(result.document["root"], str(root))
            self.assertEqual(command(records[0]), ["--version"], "the version check runs next")
        absolute = os.fsencode(self.base) + b"/home-\xff"
        cases = [("HOME", ""), ("HOME", "/"), ("HOME", absolute), ("XDG_CONFIG_HOME", ""),
                 ("XDG_CONFIG_HOME", "/"), ("XDG_CONFIG_HOME", absolute)]
        cases += [(name, value) for name in EXTENSION for value in ("", os.devnull)]
        for name, value in cases:
            env = dict(self.env)
            env[name] = value
            with self.subTest(name=name, value=value):
                result, records = self.counted("clean", root, "--json", env=env)
                self.assert_status(result, 0)
                self.assertEqual(command(records[0]), ["--version"])
            companion = "XDG_CONFIG_HOME" if name == "HOME" else "HOME"
            with self.subTest(name=name, value=value, beside=companion):
                result, records = self.counted("clean", root, env=dict(env, **{companion: "rel"}))
                self.assert_refused_human(result, config_lines(companion))
                self.assertEqual(records, [])


if __name__ == "__main__":
    unittest.main()
