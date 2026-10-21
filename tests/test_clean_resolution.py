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
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()
TEXT = clean_support.TEXT_FIXTURES

EXTENDED_ERROR_KEYS = ["error", "code", "schema_version", "observed_at", "mode", "repository", "merge_target",
                       "completeness", "apply_allowed", "refusals"]
REPOSITORY_KEYS = ["root", "common_dir", "dev", "ino", "root_valid_utf8", "common_dir_valid_utf8"]
MIB = 1048576  # LIMITS["manifest_bytes"], written here as a literal (rule 11)

# The children of D6's table, after `-C DIR` (contracts/project-clean.md, "Git children").
ROW_2 = ["rev-parse", "--show-toplevel"]
ROW_3 = ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-common-dir",
         "--show-superproject-working-tree"]
STATUS = ["status", "--porcelain=v1", "-z", "--untracked-files=normal", "--ignored=matching"]


def command(record):
    """A counted child's argument vector without its leading -c pins: `-C DIR ...`."""
    argv, at = record.argv, 0
    while at + 1 < len(argv) and argv[at] == "-c":
        at += 2
    return argv[at:]


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


if __name__ == "__main__":
    unittest.main()
