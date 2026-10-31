"""Path escaping for project clean: json_path() and human_path().

FR-039 to FR-041; tasks.md T016. Every non-ASCII input in this module is
written as an escape in the source, never as the raw character.
"""
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import unicodedata
import unittest

from clean_support import load_project

project = load_project()

ESCAPED = ("Cc", "Cf", "Zl", "Zp")

# T016's named code points: each with the escape json.dumps writes for it
# and the one the $'...' form writes for it.
NAMED = (
    ("\n", "\\n", "\\u000a"),
    ("\t", "\\t", "\\u0009"),
    ("\u0001", "\\u0001", "\\u0001"),
    ("\u007f", "\\u007f", "\\u007f"),
    ("\u0085", "\\u0085", "\\u0085"),
    ("\u200e", "\\u200e", "\\u200e"),
    ("\u2028", "\\u2028", "\\u2028"),
    ("\u202e", "\\u202e", "\\u202e"),
    ("\ufeff", "\\ufeff", "\\ufeff"),
    ("\U000e0020", "\\udb40\\udc20", "\\U000e0020"),
)

# The delta's examples of code points to escape ("Clean reports every path
# exactly or excludes it"): U+0000 to U+001F, U+007F to U+009F, U+200E,
# U+200F, U+2028, U+2029, U+202A to U+202E, U+2066 to U+2069, U+200B, U+FEFF
# and U+E0020 to U+E007F.
DELTA_EXAMPLES = (
    list(range(0x00, 0x20)) + list(range(0x7F, 0xA0))
    + [0x200E, 0x200F, 0x2028, 0x2029] + list(range(0x202A, 0x202F))
    + list(range(0x2066, 0x206A)) + [0x200B, 0xFEFF] + list(range(0xE0020, 0xE0080))
)

# Paths with no code point to escape and no undecodable byte: shell
# metacharacters, both quotes, a backslash, the four characters \xff, and
# code points of other categories (Ll, Lo, So, Zs, Co, Mn and Cn).
PLAIN = (
    b"/w/plain",
    b"/w/with space",
    b"/w/it's",
    b"/w/back\\slash",
    b"/w/\\xff",
    b"/w/$HOME `id` \"q\" !x *?[a] ~ & ; | < > # ( ) { }",
    "/w/caf\u00e9".encode("utf-8"),
    "/w/\u4e2d\u6587".encode("utf-8"),
    "/w/\U0001f600".encode("utf-8"),
    "/w/nbsp\u00a0x".encode("utf-8"),
    "/w/ideographic\u3000space".encode("utf-8"),
    "/w/pua\ue000".encode("utf-8"),
    "/w/e\u0301".encode("utf-8"),
    "/w/unassigned\u0378".encode("utf-8"),
    "/w/\U0010fffd".encode("utf-8"),
)

# Not valid UTF-8: each raw path with the text json_path gives it.
UNDECODABLE = (
    (b"/w/bad\xff", "/w/bad\\xff"),
    (b"/w/\xAB\xCD", "/w/\\xab\\xcd"),
    (b"/w/truncated\xc3", "/w/truncated\\xc3"),
    (b"/w/surrogate\xed\xa0\x80", "/w/surrogate\\xed\\xa0\\x80"),
    (b"/w/overlong\xc0\xaf", "/w/overlong\\xc0\\xaf"),
    (b"/w/beyond\xf4\x90\x80\x80", "/w/beyond\\xf4\\x90\\x80\\x80"),
    (b"/w/caf\xc3\xa9\xff", "/w/caf\u00e9\\xff"),
    (b"/w/a\\b\xff", "/w/a\\\\b\\xff"),
    (b"/w/\\xff\xff", "/w/\\\\xff\\xff"),
    (b"/w/it's\xfe", "/w/it's\\xfe"),
    (b"/w/\n\t\xff", "/w/\n\t\\xff"),
)

# Paths in the $'...' form: each raw path with the one form human_path
# gives it, in prose and in a command alike.
DOLLAR_QUOTED = tuple(
    (("/w/a" + char + "b").encode("utf-8"), "$'/w/a" + escape + "b'")
    for char, _json, escape in NAMED
) + (
    ("/w/tab\there".encode("utf-8"), "$'/w/tab\\u0009here'"),
    ("/w/\u2029".encode("utf-8"), "$'/w/\\u2029'"),
    ("/w/soft\u00adhyphen".encode("utf-8"), "$'/w/soft\\u00adhyphen'"),
    ("/w/\u2066x\u2069".encode("utf-8"), "$'/w/\\u2066x\\u2069'"),
    ("/w/it's\t".encode("utf-8"), "$'/w/it\\'s\\u0009'"),
    ("/w/a\\b\t".encode("utf-8"), "$'/w/a\\\\b\\u0009'"),
    ("/w/\u00011".encode("utf-8"), "$'/w/\\u00011'"),
    ("/w/\U000e007f0".encode("utf-8"), "$'/w/\\U000e007f0'"),
    ("/w/caf\u00e9\u200f".encode("utf-8"), "$'/w/caf\u00e9\\u200f'"),
    ("/w/\u202eA".encode("utf-8"), "$'/w/\\u202eA'"),
    (b"/w/bad\xff", "$'/w/bad\\xff'"),
    (b"/w/\xAB", "$'/w/\\xab'"),
    (b"/w/a\\'b\xfe", "$'/w/a\\\\\\'b\\xfe'"),
    (b"/w/caf\xc3\xa9\xff", "$'/w/caf\u00e9\\xff'"),
    (b"/w/\t\xff", "$'/w/\\u0009\\xff'"),
    (b"/w/\xffff", "$'/w/\\xffff'"),
)

HEX = {"x": 2, "u": 4, "U": 8}


def every_code_point(start=0):
    """Every code point from start up, surrogates excepted, as one string."""
    return "".join(chr(point) for point in range(start, 0x110000)
                   if not 0xD800 <= point <= 0xDFFF)


def bytes_of_json_text(text, valid):
    """The test's own reading of FR-039: the bytes json_path's text names.
    Valid text is UTF-8; otherwise two backslashes are one backslash and
    \\xHH, in lower case, is one byte."""
    if valid:
        return text.encode("utf-8")
    out = bytearray()
    index = 0
    while index < len(text):
        char = text[index]
        if char != "\\":
            out += char.encode("utf-8")
            index += 1
        elif text[index + 1] == "\\":
            out += b"\\"
            index += 2
        else:
            digits = text[index + 2:index + 4]
            if text[index + 1] != "x" or not re.fullmatch("[0-9a-f]{2}", digits):
                raise AssertionError(f"bad escape at {index} in {text!a}")
            out.append(int(digits, 16))
            index += 4
    return bytes(out)


def bytes_of_dollar_quote(form):
    """The test's own reading of the $'...' form, as bash reads it in a
    UTF-8 locale, for the escapes FR-041 allows, each in lower case."""
    if not (form.startswith("$'") and form.endswith("'") and len(form) >= 3):
        raise AssertionError(f"not a $'...' form: {form!a}")
    body = form[2:-1]
    out = bytearray()
    index = 0
    while index < len(body):
        char = body[index]
        if char == "'":
            raise AssertionError(f"raw single quote at {index} in {form!a}")
        if char != "\\":
            out += char.encode("utf-8")
            index += 1
            continue
        kind = body[index + 1]
        if kind in "\\'":
            out += kind.encode("ascii")
            index += 2
            continue
        width = HEX.get(kind)
        digits = body[index + 2:index + 2 + (width or 0)]
        if width is None or not re.fullmatch(f"[0-9a-f]{{{width}}}", digits):
            raise AssertionError(f"bad escape at {index} in {form!a}")
        if kind == "x":
            out.append(int(digits, 16))
        else:
            out += chr(int(digits, 16)).encode("utf-8")
        index += 2 + width
    return bytes(out)


class EscapingTests(unittest.TestCase):
    def test_clean_json_path_returns_valid_utf_8_exactly(self):
        named = tuple(("/w/a" + char + "b").encode("utf-8") for char, _json, _human in NAMED)
        for raw in PLAIN + named:
            with self.subTest(raw=raw):
                text, valid = project.json_path(raw)
                self.assertIs(valid, True)
                self.assertIsInstance(text, str)
                self.assertEqual(text, raw.decode("utf-8"))
                document = json.dumps({"path": text, "path_valid_utf8": valid})
                self.assertEqual(json.loads(document)["path"].encode("utf-8"), raw)

    def test_clean_json_path_writes_each_named_code_point_as_an_escape(self):
        for char, escape, _human in NAMED:
            raw = ("/w/a" + char + "b").encode("utf-8")
            with self.subTest(code_point=f"U+{ord(char):04X}"):
                text, valid = project.json_path(raw)
                self.assertIs(valid, True)
                document = json.dumps({"path": text, "path_valid_utf8": valid})
                self.assertNotIn(char, document)
                self.assertTrue(document.isascii(), document)
                self.assertIn('"/w/a' + escape + 'b"', document)
                self.assertEqual(json.loads(document)["path"], raw.decode("utf-8"))

    def test_clean_json_path_writes_no_code_point_to_escape_raw(self):
        every = every_code_point()
        text, valid = project.json_path(every.encode("utf-8"))
        self.assertIs(valid, True)
        self.assertEqual(text, every)
        document = json.dumps(text)
        self.assertEqual({char for char in document if not " " <= char <= "~"}, set())
        self.assertEqual(json.loads(document), every)

    def test_clean_json_path_escapes_undecodable_bytes(self):
        for raw, expected in UNDECODABLE:
            with self.subTest(raw=raw):
                text, valid = project.json_path(raw)
                self.assertIs(valid, False)
                self.assertEqual(text, expected)
                text.encode("utf-8")  # no lone surrogate reaches a document
                self.assertEqual(bytes_of_json_text(text, valid), raw)
                document = json.dumps({"path": text, "path_valid_utf8": valid})
                self.assertTrue(document.isascii(), document)
                self.assertNotIn("\n", document)
                self.assertNotIn("\t", document)
                self.assertEqual(json.loads(document), {"path": expected, "path_valid_utf8": False})

    def test_clean_json_path_flag_tells_an_escape_from_its_four_characters(self):
        self.assertEqual(project.json_path(b"/w/\\xff"), ("/w/\\xff", True))
        self.assertEqual(project.json_path(b"/w/\xff"), ("/w/\\xff", False))
        self.assertEqual(project.json_path(b"/w/\\xff\xff"), ("/w/\\\\xff\\xff", False))
        self.assertEqual(project.json_path(b"/w/\xff\xff"), ("/w/\\xff\\xff", False))

    def test_clean_human_path_prints_a_plain_path_verbatim_and_quoted(self):
        for raw in PLAIN:
            text = raw.decode("utf-8")
            with self.subTest(raw=raw):
                self.assertEqual([char for char in text if unicodedata.category(char) in ESCAPED], [])
                self.assertEqual(project.human_path(raw), text)
                self.assertEqual(project.human_path(raw, command=False), text)
                self.assertEqual(project.human_path(raw, command=True), shlex.quote(text))

    def test_clean_human_path_writes_the_dollar_quote_form(self):
        for raw, expected in DOLLAR_QUOTED:
            with self.subTest(raw=raw):
                self.assertEqual(project.human_path(raw), expected)
                self.assertEqual(project.human_path(raw, command=True), expected)
                self.assertEqual(bytes_of_dollar_quote(expected), raw)

    def test_clean_human_path_escapes_the_delta_s_examples(self):
        for point in DELTA_EXAMPLES:
            char = chr(point)
            with self.subTest(code_point=f"U+{point:04X}"):
                self.assertIn(unicodedata.category(char), ESCAPED)
                escape = f"\\u{point:04x}" if point <= 0xFFFF else f"\\U{point:08x}"
                raw = ("/w/" + char).encode("utf-8")
                self.assertEqual(project.human_path(raw), "$'/w/" + escape + "'")
                self.assertEqual(project.human_path(raw, command=True), "$'/w/" + escape + "'")

    def test_clean_human_path_escapes_exactly_the_four_categories(self):
        every = every_code_point()
        escaped = [char for char in every if unicodedata.category(char) in ESCAPED]
        plain = "".join(char for char in every if unicodedata.category(char) not in ESCAPED)
        for char, _json, _human in NAMED:
            self.assertIn(char, escaped)
        self.assertEqual(project.human_path(plain.encode("utf-8")), plain)
        self.assertEqual(project.human_path(plain.encode("utf-8"), command=True), shlex.quote(plain))
        for char in escaped:
            point = ord(char)
            escape = f"\\u{point:04x}" if point <= 0xFFFF else f"\\U{point:08x}"
            self.assertEqual(project.human_path(char.encode("utf-8")), "$'" + escape + "'")
        whole = project.human_path(every.encode("utf-8"))
        self.assertEqual(set(whole) & set(escaped), set())
        self.assertEqual(bytes_of_dollar_quote(whole), every.encode("utf-8"))

    def test_clean_human_path_reads_back_through_the_shell(self):
        bash = shutil.which("bash")
        if bash is None:
            self.skipTest("bash is not on PATH")
        env = dict(os.environ, LC_ALL="C.UTF-8")
        check = subprocess.run([bash, "--norc", "--noprofile", "-c", "printf '%s' $'\\u00e9'"],
                               capture_output=True, env=env, timeout=10)
        if check.stdout != b"\xc3\xa9":
            self.skipTest("bash does not read \\u escapes in the C.UTF-8 locale here")
        quoted = [raw for raw, _form in DOLLAR_QUOTED]
        quoted += [("/w/" + chr(point)).encode("utf-8") for point in DELTA_EXAMPLES if point]
        quoted += [b"/w/" + bytes([byte]) + b"0" for byte in range(0x80, 0x100)]
        quoted += [b"/w/" + bytes(range(1, 0x80)) + b"\xff"]
        for shell, paths in ((bash, quoted + list(PLAIN)), (shutil.which("sh"), PLAIN)):
            if shell is None:
                continue
            with self.subTest(shell=shell):
                script = b"".join(b"printf '%s\\0' " + project.human_path(raw, command=True).encode("utf-8")
                                  + b"\n" for raw in paths)
                result = subprocess.run([shell, "-s"], input=script, capture_output=True, env=env, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.split(b"\0")[:-1], list(paths))

    def test_clean_escaping_takes_bytes_text_or_path_objects(self):
        for raw in (b"/w/bad\xff\t", b"/w/plain", "/w/\u202e".encode("utf-8")):
            text = os.fsdecode(raw)
            with self.subTest(raw=raw):
                for given in (text, Path(text), bytearray(raw), memoryview(raw)):
                    self.assertEqual(project.json_path(given), project.json_path(raw))
                    self.assertEqual(project.human_path(given), project.human_path(raw))
                    self.assertEqual(project.human_path(given, command=True),
                                     project.human_path(raw, command=True))

    def test_clean_escaped_output_holds_no_lone_surrogate(self):
        for raw, _expected in UNDECODABLE:
            with self.subTest(raw=raw):
                project.json_path(raw)[0].encode("utf-8")
                project.human_path(raw).encode("utf-8")
                project.human_path(raw, command=True).encode("utf-8")
        ascii_only = b"/w/\t\xff\xfe" + "\u202e\U000e0020".encode("utf-8")
        self.assertTrue(project.human_path(ascii_only).isascii())


if __name__ == "__main__":
    unittest.main()
