"""Lane D of feature 004 (T014): the five incremental parsers of design D2.

FR-062: a recorded stream gives the same records and the same bound_reached
fed one byte at a time, in small chunks and whole. The byte literals below were
recorded from throwaway repositories (GIT_CONFIG_NOSYSTEM=1,
GIT_CONFIG_GLOBAL=/dev/null, a fixed author, committer and date) under Git
2.43.0 and Git 2.36.6, which printed every one of them identically; each
repository's temporary directory is written /rec. The status probes ran with
the two status pins, and the first, to print a copy record, with
`-c status.renames=copies` too. The bounds run at their real sizes (rule 6).
"""
import builtins
import os
import subprocess
import unittest
from unittest import mock

from clean_support import load_project

project = load_project()

CHUNK_SIZES = (1, 2, 3, 7, None)  # None feeds the whole stream at once

# status --porcelain=v1 -z --untracked-files=normal --ignored=matching: a
# modified file, a rename, two deletions, a staged change, a copy, untracked
# files whose names hold 0xFF and a line feed, another untracked file and an
# ignored one.
STATUS = (b" M a.txt\x00R  b2.txt\x00b.txt\x00 D c.txt\x00 D d.txt\x00M  f.txt\x00"
          b"C  f2.txt\x00f.txt\x00?? bad\xff.txt\x00?? new\nline.txt\x00?? u.txt\x00"
          b"!! i.log\x00")
# Every tracked file deleted in the working tree, an ignored file left (D4).
STATUS_DELETED = b" D src/y.txt\x00 D x.txt\x00!! build.log\x00"
# A clean worktree holding ten ignored files, two names holding a line feed
# and 0xFF.
STATUS_IGNORED = (b"!! a\nb.log\x00!! c\xff.log\x00!! d0.log\x00!! d1.log\x00!! d2.log\x00"
                  b"!! d3.log\x00!! d4.log\x00!! d5.log\x00!! d6.log\x00!! d7.log\x00")

HEAD = "e20e62cda8588680653b5a27f98bd475d0cfb52d"
# worktree list --porcelain -z: the main worktree, a detached one, one locked
# without a reason, one locked with a reason and a prunable one.
REGISTRY = (
    b"worktree /rec/w\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
    b"branch refs/heads/main\x00\x00"
    b"worktree /rec/w-detached\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
    b"detached\x00\x00"
    b"worktree /rec/w-held\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
    b"branch refs/heads/held\x00locked\x00\x00"
    b"worktree /rec/w-locked\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
    b"branch refs/heads/feature\x00locked on a stick\x00\x00"
    b"worktree /rec/w-prunable\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
    b"branch refs/heads/gone\x00prunable gitdir file points to non-existent location\x00\x00")
# The same of a bare repository with one linked worktree.
REGISTRY_BARE = (b"worktree /rec/b.git\x00bare\x00\x00"
                 b"worktree /rec/b-main\x00HEAD e20e62cda8588680653b5a27f98bd475d0cfb52d\x00"
                 b"branch refs/heads/main\x00\x00")

MAIN = "35af49a6fca41fc9f3059f693377c194baa75125"
AB = "59ea804ac09bad4569c051cbff90de48cb15164c"
ORIGIN_AB = "b206283c6f3c019d0ac317afaa457504936792ba"
# for-each-ref over refs/heads and refs/remotes in design D6's row 6 format:
# ab ahead 2 and behind 1, local with no upstream, main level with its
# upstream, old whose upstream is gone, and origin/HEAD a symref.
REFS = (
    b"refs/heads/ab\x0059ea804ac09bad4569c051cbff90de48cb15164c\x00\x00"
    b"refs/remotes/origin/ab\x00origin/ab\x00ahead 2, behind 1\n"
    b"refs/heads/local\x0035af49a6fca41fc9f3059f693377c194baa75125\x00\x00\x00\x00\n"
    b"refs/heads/main\x0035af49a6fca41fc9f3059f693377c194baa75125\x00\x00"
    b"refs/remotes/origin/main\x00origin/main\x00\n"
    b"refs/heads/old\x0035af49a6fca41fc9f3059f693377c194baa75125\x00\x00"
    b"refs/remotes/origin/old\x00origin/old\x00gone\n"
    b"refs/remotes/origin/HEAD\x0035af49a6fca41fc9f3059f693377c194baa75125\x00"
    b"refs/remotes/origin/main\x00\x00\x00\n"
    b"refs/remotes/origin/ab\x00b206283c6f3c019d0ac317afaa457504936792ba\x00\x00\x00\x00\n"
    b"refs/remotes/origin/main\x0035af49a6fca41fc9f3059f693377c194baa75125\x00\x00\x00\x00\n")
# for-each-ref --merged=MAIN --format=%(refname) refs/heads in the same clone.
MERGED = b"refs/heads/local\nrefs/heads/main\nrefs/heads/old\n"
# ls-files -v --stage -z: H, h (assume-unchanged), S (skip-worktree), then a
# gitlink.
HIDDEN = (b"H 100644 5883f20277d3f484a0469500aa541348f29e2e6a 0\th1.txt\x00"
          b"h 100644 93a1add2f8e982e06796e2766a4726acb3464fac 0\th2.txt\x00"
          b"S 100644 ff57e098f6f3345ee23c5ebf696e86b204bac684 0\ts1.txt\x00"
          b"H 160000 b15846d4ee74d0dc4a22fe7a82f709c3df177e61 0\tzsub\x00")
HIDDEN_ENTRY = b"%s 100644 5883f20277d3f484a0469500aa541348f29e2e6a 0\t%s\x00"


def recorded():
    return ((project.StatusParser, STATUS), (project.StatusParser, STATUS_DELETED),
            (project.StatusParser, STATUS_IGNORED), (project.WorktreeListParser, REGISTRY),
            (project.WorktreeListParser, REGISTRY_BARE), (project.RefParser, REFS),
            (project.MergedSetParser, MERGED), (project.HiddenStateParser, HIDDEN))


def summary(dirty, ignored_files, truncated, samples, records, deletions_only=False):
    """StatusParser.finish()'s result, the keys in its order."""
    return {"dirty": dirty, "ignored_files": ignored_files,
            "ignored_files_truncated": truncated, "ignored_samples": samples,
            "records": records, "deletions_only": deletions_only}


def entry(path, head=HEAD, branch=None, **flags):
    """WorktreeListParser's entry for path, every flag false and reason None
    unless named."""
    result = {"path": path, "head": head, "branch": branch, "bare": False,
              "detached": False, "locked": False, "locked_reason": None,
              "prunable": False, "prunable_reason": None}
    result.update(flags)
    return result


def ref(refname, objectname, upstream=None, short=None, present=None, ahead=None,
        behind=None, symref=None):
    return {"refname": refname, "objectname": objectname, "symref": symref,
            "upstream": upstream, "upstream_short": short, "remote_present": present,
            "ahead": ahead, "behind": behind}


def ignored(count):
    return b"".join(b"!! cache/%04d.log\x00" % i for i in range(count))


def untracked(count):
    return b"".join(b"?? new/%04d.txt\x00" % i for i in range(count))


class CleanParserTests(unittest.TestCase):

    def feed(self, parser_class, stream, size):
        """A new parser fed stream in chunks of size bytes (whole when None);
        returns finish()'s result, or the ParseError it raised, and
        bound_reached. feed() itself must never raise."""
        parser = parser_class()
        step = size or max(len(stream), 1)
        for start in range(0, len(stream), step):
            parser.feed(stream[start:start + step])
        try:
            result = parser.finish()
        except project.ParseError as exc:
            result = exc
        return result, parser.bound_reached

    def assert_parses(self, parser_class, stream, expected, bound=False):
        for size in CHUNK_SIZES:
            with self.subTest(parser=parser_class.__name__, chunk=size or "whole",
                              stream=stream[:48]):
                result, reached = self.feed(parser_class, stream, size)
                self.assertEqual(result, expected)
                self.assertIs(reached, bound)

    def assert_fails(self, parser_class, stream):
        for size in CHUNK_SIZES:
            with self.subTest(parser=parser_class.__name__, chunk=size or "whole",
                              stream=stream[:48]):
                result, reached = self.feed(parser_class, stream, size)
                self.assertIsInstance(result, project.ParseError)
                self.assertIs(reached, False)

    def test_clean_status_parser_reads_recorded_streams(self):
        self.assert_parses(project.StatusParser, STATUS, {
            "dirty": True, "ignored_files": 1, "ignored_files_truncated": False,
            "ignored_samples": [b"i.log"], "records": 10, "deletions_only": False})
        self.assert_parses(project.StatusParser, STATUS_DELETED,
                           summary(True, 1, False, [b"build.log"], 3, deletions_only=True))
        self.assert_parses(project.StatusParser, STATUS_IGNORED, summary(
            False, 10, False, [b"a\nb.log", b"c\xff.log", b"d0.log", b"d1.log", b"d2.log",
                               b"d3.log", b"d4.log", b"d5.log"], 10))
        self.assert_parses(project.StatusParser, b"", summary(False, 0, False, [], 0))

    def test_clean_status_parser_stops_at_the_65th_ignored_record(self):
        self.assertEqual(project.LIMITS["ignored_entries"], 64)
        self.assertEqual(project.LIMITS["ignored_samples"], 8)
        samples = [b"cache/%04d.log" % i for i in range(8)]
        at_bound = summary(False, 64, True, samples, 64)
        for count in (65, 70, 5000):
            self.assert_parses(project.StatusParser, ignored(count), at_bound, bound=True)
        self.assert_parses(project.StatusParser, ignored(64), summary(False, 64, False, samples, 64))
        self.assert_parses(project.StatusParser, untracked(1) + ignored(65),
                           summary(True, 64, True, samples, 65), bound=True)
        # The bound comes with the 65th record's terminator, and nothing after
        # it is read, a malformed or truncated record included.
        stream = ignored(65)
        parser = project.StatusParser()
        parser.feed(stream[:-1])
        self.assertIs(parser.bound_reached, False)
        parser.feed(stream[-1:] + b"not a record\x00?? half")
        self.assertIs(parser.bound_reached, True)
        parser.feed(b"!! more.log\x00")
        self.assertEqual(parser.finish(), at_bound)

    def test_clean_status_parser_stops_at_the_4097th_record(self):
        self.assertEqual(project.LIMITS["status_records"], 4096)
        self.assert_parses(project.StatusParser, untracked(4097),
                           summary(True, None, True, [], 4096), bound=True)
        self.assert_parses(project.StatusParser, untracked(4096),
                           summary(True, 0, False, [], 4096))
        # A rename or copy and its source path are one record.
        renames = b"".join(b"R  new/%04d.txt\x00old/%04d.txt\x00" % (i, i) for i in range(4097))
        self.assert_parses(project.StatusParser, renames,
                           summary(True, None, True, [], 4096), bound=True)
        # Ignored records read before the bound: their count is a lower bound.
        self.assert_parses(project.StatusParser, untracked(4090) + ignored(10), summary(
            True, 6, True, [b"cache/%04d.log" % i for i in range(6)], 4096), bound=True)

    def test_clean_status_parser_follows_d2_and_d4(self):
        parser = project.StatusParser()
        self.assertIsNone(parser.dirty)
        parser.feed(b"!! a.log\x00")
        self.assertIs(parser.dirty, False)  # an ignored record arrived first
        parser.feed(b" M x.txt\x00")
        self.assertIs(parser.dirty, True)  # any other record makes it dirty
        cases = (
            (b" D x.txt\x00?? u.txt\x00", summary(True, 0, False, [], 2)),
            (b"?? u.txt\x00 D x.txt\x00", summary(True, 0, False, [], 2)),
            (b"D  x.txt\x00", summary(True, 0, False, [], 1)),
            (b" M x.txt\x00", summary(True, 0, False, [], 1)),
            (b"!! a.log\x00", summary(False, 1, False, [b"a.log"], 1)),
            (b" D x.txt\x00 D y.txt\x00", summary(True, 0, False, [], 2, deletions_only=True)),
            # Ignored records leave the deletion flag alone wherever they stand.
            (b"!! a.log\x00 D x.txt\x00", summary(True, 1, False, [b"a.log"], 2, deletions_only=True)),
        )
        for stream, expected in cases:
            self.assert_parses(project.StatusParser, stream, expected)
        # A stream stopped at its bound is judged on the records read.
        deleted = b"".join(b" D f/%04d.txt\x00" % i for i in range(4096))
        self.assert_parses(project.StatusParser, deleted + b"?? late.txt\x00",
                           summary(True, None, True, [], 4096, deletions_only=True), bound=True)
        self.assert_parses(project.StatusParser, b"?? early.txt\x00" + deleted,
                           summary(True, None, True, [], 4096), bound=True)

    def test_clean_status_parser_reads_limits_when_made(self):
        bounds = {"ignored_entries": 2, "status_records": 5, "ignored_samples": 1}
        with mock.patch.dict(project.LIMITS, bounds):
            by_ignored = project.StatusParser()
            by_records = project.StatusParser()
        by_ignored.feed(b"!! a.log\x00!! b.log\x00!! c.log\x00")
        self.assertIs(by_ignored.bound_reached, True)
        self.assertEqual(by_ignored.finish(), summary(False, 2, True, [b"a.log"], 2))
        by_records.feed(untracked(6))
        self.assertEqual(by_records.finish(), summary(True, None, True, [], 5))
        unpatched = project.StatusParser()
        unpatched.feed(b"!! a.log\x00!! b.log\x00!! c.log\x00")
        self.assertIs(unpatched.bound_reached, False)
        self.assertEqual(unpatched.finish(),
                         summary(False, 3, False, [b"a.log", b"b.log", b"c.log"], 3))

    def test_clean_worktree_list_parser_reads_recorded_streams(self):
        self.assert_parses(project.WorktreeListParser, REGISTRY, [
            {"path": b"/rec/w", "head": HEAD, "branch": b"refs/heads/main", "bare": False,
             "detached": False, "locked": False, "locked_reason": None, "prunable": False,
             "prunable_reason": None},
            entry(b"/rec/w-detached", detached=True),
            entry(b"/rec/w-held", branch=b"refs/heads/held", locked=True),
            entry(b"/rec/w-locked", branch=b"refs/heads/feature", locked=True,
                  locked_reason=b"on a stick"),
            entry(b"/rec/w-prunable", branch=b"refs/heads/gone", prunable=True,
                  prunable_reason=b"gitdir file points to non-existent location"),
        ])
        self.assert_parses(project.WorktreeListParser, REGISTRY_BARE, [
            entry(b"/rec/b.git", head=None, bare=True),
            entry(b"/rec/b-main", branch=b"refs/heads/main"),
        ])
        # A path holding a line feed and 0xFF stays raw bytes; an attribute
        # this parser does not know is skipped.
        self.assert_parses(project.WorktreeListParser,
                           b"worktree /rec/x\ny\xff\x00HEAD " + HEAD.encode()
                           + b"\x00branch refs/heads/x\x00future value\x00\x00",
                           [entry(b"/rec/x\ny\xff", branch=b"refs/heads/x")])
        self.assert_parses(project.WorktreeListParser, b"", [])

    def test_clean_ref_parser_reads_recorded_streams(self):
        self.assert_parses(project.RefParser, REFS, [
            {"refname": b"refs/heads/ab", "objectname": AB, "symref": None,
             "upstream": b"refs/remotes/origin/ab", "upstream_short": b"origin/ab",
             "remote_present": True, "ahead": 2, "behind": 1},
            ref(b"refs/heads/local", MAIN),
            ref(b"refs/heads/main", MAIN, b"refs/remotes/origin/main", b"origin/main", True, 0, 0),
            ref(b"refs/heads/old", MAIN, b"refs/remotes/origin/old", b"origin/old", False),
            ref(b"refs/remotes/origin/HEAD", MAIN, symref=b"refs/remotes/origin/main"),
            ref(b"refs/remotes/origin/ab", ORIGIN_AB),
            ref(b"refs/remotes/origin/main", MAIN),
        ])
        upstream = b"refs/heads/x\x00" + MAIN.encode() + b"\x00\x00refs/remotes/o/x\x00o/x\x00"
        self.assert_parses(project.RefParser, upstream + b"ahead 3\n" + upstream + b"behind 4\n", [
            ref(b"refs/heads/x", MAIN, b"refs/remotes/o/x", b"o/x", True, 3, 0),
            ref(b"refs/heads/x", MAIN, b"refs/remotes/o/x", b"o/x", True, 0, 4),
        ])
        sha256 = "0123456789abcdef" * 4
        self.assert_parses(project.RefParser, b"refs/heads/y\x00" + sha256.encode() + b"\x00\x00\x00\x00\n",
                           [ref(b"refs/heads/y", sha256)])
        self.assert_parses(project.RefParser, b"", [])

    def test_clean_merged_set_parser_reads_recorded_streams(self):
        self.assert_parses(project.MergedSetParser, MERGED, frozenset(
            {b"refs/heads/local", b"refs/heads/main", b"refs/heads/old"}))
        self.assert_parses(project.MergedSetParser, b"refs/heads/\xffx\n", frozenset({b"refs/heads/\xffx"}))
        self.assert_parses(project.MergedSetParser, b"", frozenset())

    def test_clean_hidden_state_parser_reads_recorded_streams(self):
        self.assert_parses(project.HiddenStateParser, HIDDEN,
                           {"gitlink": True, "hidden": True, "entries": 3}, bound=True)
        before_gitlink = HIDDEN[:HIDDEN.index(b"H 160000")]
        self.assert_parses(project.HiddenStateParser, before_gitlink,
                           {"gitlink": False, "hidden": True, "entries": 3})
        self.assert_parses(project.HiddenStateParser, before_gitlink.split(b"h 100644")[0],
                           {"gitlink": False, "hidden": False, "entries": 1})
        for tag in (b"h", b"s", b"S", b"m"):
            self.assert_parses(project.HiddenStateParser, HIDDEN_ENTRY % (tag, b"a\nb\xff"),
                               {"gitlink": False, "hidden": True, "entries": 1})
        for tag in (b"H", b"M", b"R", b"C", b"K"):
            self.assert_parses(project.HiddenStateParser, HIDDEN_ENTRY % (tag, b"p"),
                               {"gitlink": False, "hidden": False, "entries": 1})
        # It stops at the first gitlink: nothing after it is read.
        gitlink = HIDDEN[HIDDEN.index(b"H 160000"):]
        self.assert_parses(project.HiddenStateParser,
                           gitlink + HIDDEN_ENTRY % (b"h", b"later") + b"garbage\x00half",
                           {"gitlink": True, "hidden": False, "entries": 0}, bound=True)
        self.assert_parses(project.HiddenStateParser, b"",
                           {"gitlink": False, "hidden": False, "entries": 0})

    def test_clean_hidden_state_parser_names_the_directories_that_hold_an_entry(self):
        # Brett Heap's Q2 (2), lead R-380: `directories` holds every directory
        # above an entry read before the bound, the top level aside, so that
        # gate 9 can lstat `<dir>/.git` in each; a gitlink ends the listing.
        stream = b"".join(HIDDEN_ENTRY % (b"H", name) for name in (
            b"top.txt", b"a/b/c.txt", b"a/d.txt", b"x/y/z/w.txt", b"a\nb/\xff/f"))
        for size in CHUNK_SIZES:
            with self.subTest(chunk=size or "whole"):
                parser = project.HiddenStateParser()
                for at in range(0, len(stream), size or len(stream)):
                    parser.feed(stream[at:at + (size or len(stream))])
                self.assertEqual(parser.finish(), {"gitlink": False, "hidden": False, "entries": 5})
                self.assertEqual(parser.directories, {b"a", b"a/b", b"x", b"x/y", b"x/y/z", b"a\nb", b"a\nb/\xff"})
        parser = project.HiddenStateParser()
        parser.feed(HIDDEN_ENTRY % (b"H", b"d/one") + HIDDEN[HIDDEN.index(b"H 160000"):] + HIDDEN_ENTRY % (b"H", b"e/two"))
        self.assertEqual((parser.finish()["gitlink"], parser.directories), (True, {b"d"}))

    def test_clean_unbounded_parsers_never_reach_a_bound(self):
        many = b"".join(b"refs/heads/b%05d\n" % i for i in range(5000))
        self.assert_parses(project.MergedSetParser, many,
                           frozenset(b"refs/heads/b%05d" % i for i in range(5000)))
        rows = b"".join(b"worktree /rec/r%04d\x00HEAD %s\x00detached\x00\x00" % (i, HEAD.encode())
                        for i in range(300))
        self.assert_parses(project.WorktreeListParser, rows,
                           [entry(b"/rec/r%04d" % i, detached=True) for i in range(300)])

    def test_clean_parsers_fail_a_truncated_last_record_at_finish(self):
        for parser_class, stream in recorded():
            self.assert_fails(parser_class, stream[:-1])
            if stream is not HIDDEN:
                self.assert_fails(parser_class, stream + b"r")
        # A truncated record after the bound is never read.
        self.assert_parses(project.HiddenStateParser, HIDDEN + b"r",
                           {"gitlink": True, "hidden": True, "entries": 3}, bound=True)
        self.assert_fails(project.StatusParser, b" M a.txt\x00R  b2.txt\x00")  # no source path
        self.assert_fails(project.StatusParser, b"R  b2.txt\x00b.t")
        self.assert_fails(project.StatusParser, ignored(64)[:-1])
        self.assert_fails(project.WorktreeListParser, REGISTRY_BARE[:-1])  # entry not ended
        self.assert_fails(project.WorktreeListParser, b"worktree /rec/w\x00")
        self.assert_fails(project.RefParser, REFS[:REFS.index(b"\n") - 4])
        self.assert_fails(project.HiddenStateParser, HIDDEN[:HIDDEN.index(b"\tzsub")])

    def test_clean_parsers_fail_a_malformed_record_at_finish(self):
        sha = MAIN.encode()
        cases = (
            (project.StatusParser, b"?? \x00"),
            (project.StatusParser, b"?\x00"),
            (project.StatusParser, b"XY a.txt\x00"),
            (project.StatusParser, b"??_a.txt\x00"),
            (project.StatusParser, b"R  new.txt\x00\x00"),
            (project.WorktreeListParser, b"HEAD " + sha + b"\x00\x00"),
            (project.WorktreeListParser, b"worktree \x00\x00"),
            (project.WorktreeListParser, b"worktree /rec/w\x00HEAD 123\x00\x00"),
            (project.WorktreeListParser, b"worktree /rec/w\x00branch \x00\x00"),
            (project.WorktreeListParser, b"worktree /rec/w\x00\x00\x00"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00\x00\n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00\x00\x00\x00\n"),
            (project.RefParser, b"\x00" + sha + b"\x00\x00\x00\x00\n"),
            (project.RefParser, b"refs/heads/x\x00HEAD\x00\x00\x00\x00\n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00refs/remotes/o/x\x00\x00\n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00\x00\x00gone\n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00refs/remotes/o/x\x00o/x\x00ahead two\n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00refs/remotes/o/x\x00o/x\x00, \n"),
            (project.RefParser, b"refs/heads/x\x00" + sha + b"\x00\x00refs/remotes/o/x\x00o/x\x00ahead 1, \n"),
            (project.MergedSetParser, b"refs/heads/main\n\n"),
            (project.HiddenStateParser, b"H 100644 zz 0\tp\x00"),
            (project.HiddenStateParser, b"H 100644 " + sha + b" 0 p\x00"),
            (project.HiddenStateParser, b"1 100644 " + sha + b" 0\tp\x00"),
        )
        for parser_class, stream in cases:
            self.assert_fails(parser_class, stream)
            # Nothing after the malformed record is read: a valid stream fed
            # after it changes nothing.
            parser = parser_class()
            parser.feed(stream)
            for valid_class, valid in recorded():
                if valid_class is parser_class:
                    parser.feed(valid)
            self.assertIs(parser.bound_reached, False)
            with self.assertRaises(project.ParseError):
                parser.finish()

    def test_clean_parsers_do_no_io(self):
        def refuse(*args, **kwargs):
            raise AssertionError("a parser did I/O")
        streams = (*recorded(), (project.StatusParser, ignored(70)),
                   (project.StatusParser, STATUS[:-1]), (project.RefParser, b"\n"))
        with mock.patch.object(builtins, "open", refuse), mock.patch.object(os, "open", refuse), \
                mock.patch.object(os, "read", refuse), mock.patch.object(subprocess, "Popen", refuse):
            for parser_class, stream in streams:
                for size in CHUNK_SIZES:
                    self.feed(parser_class, stream, size)


if __name__ == "__main__":
    unittest.main()
