"""Lane C: the scrubbed environment and the pins of every Git child (T012).

FR-054; design D6, D9 and D11; contracts/project-clean.md, "Git children";
lead rulings R-21, R-23, R-25 and R-28. The push kind follows draft PR #19
(LQ-3, an assumption until Brett Heap's word).
"""
import os
import unittest
from unittest import mock

import clean_support

project = clean_support.load_project()

# The contract's list, character for character and in its order
# (contracts/project-clean.md, "Git children").
SCRUB = tuple("""
GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_CONFIG GIT_CONFIG_PARAMETERS
GIT_CONFIG_COUNT GIT_OBJECT_DIRECTORY GIT_DIR GIT_WORK_TREE
GIT_IMPLICIT_WORK_TREE GIT_GRAFT_FILE GIT_INDEX_FILE GIT_NO_REPLACE_OBJECTS
GIT_REPLACE_REF_BASE GIT_PREFIX GIT_SHALLOW_FILE GIT_COMMON_DIR
GIT_INTERNAL_SUPER_PREFIX GIT_ALLOW_PROTOCOL
""".split())

# The seven protocol pins and the two status pins, as the contract spells them.
PROTOCOL = tuple("""
-c protocol.allow=never -c protocol.file.allow=never
-c protocol.ssh.allow=never -c protocol.git.allow=never
-c protocol.http.allow=never -c protocol.https.allow=never
-c protocol.ext.allow=never
""".split())
STATUS = ("-c", "core.untrackedCache=false", "-c", "core.fsmonitor=false")

# Design D9's removal vector up to `-C`, character for character.
D9_REMOVAL = """git -c
status.showUntrackedFiles=normal -c core.untrackedCache=false -c
core.fsmonitor=false -c protocol.allow=never -c protocol.file.allow=never -c
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
    def test_clean_scrub_removes_the_seventeen_names(self):
        self.assertEqual(project.GIT_SCRUB, SCRUB)
        self.assertEqual(len(set(SCRUB)), 17)
        # The caller's environment, built whole: all seventeen, the two config
        # files, and names the scrub never touches; no GIT_OPTIONAL_LOCKS.
        caller = {name: "caller-" + name for name in SCRUB}
        caller.update(GIT_CONFIG_GLOBAL="/cfg/global", GIT_CONFIG_SYSTEM="/cfg/system",
                      GIT_CONFIG_NOSYSTEM="1", PATH="/usr/bin:/bin",
                      LANE_C_UNRELATED="kept")
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
                if kind not in READ_ONLY:
                    self.assertNotIn("GIT_OPTIONAL_LOCKS", env)
        # The push child keeps GIT_ALLOW_PROTOCOL only: the other sixteen go.
        self.assertEqual([name for name in SCRUB if name in envs["push"]],
                         ["GIT_ALLOW_PROTOCOL"])
        # A read-only probe sets GIT_OPTIONAL_LOCKS=0 over a caller's value.
        locked = {"GIT_OPTIONAL_LOCKS": "1", "PATH": "/usr/bin:/bin"}
        with mock.patch.dict(os.environ, locked, clear=True):
            for kind in READ_ONLY:
                self.assertEqual(project.git_env(kind),
                                 {"GIT_OPTIONAL_LOCKS": "0", "PATH": "/usr/bin:/bin"})
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


if __name__ == "__main__":
    unittest.main()
