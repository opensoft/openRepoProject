#!/usr/bin/env python3
"""Run project's main() in this process, its TIMING table replaced (lead rulings R-26, R-29).

    python3 tests/launch_project.py [--timing=JSON] ARGS...

JSON is an object of TIMING keys and numbers. When the first argument is
--timing=JSON, TIMING becomes a new dict: the real table updated by the object's
values as floats. An unknown key is refused by name, so a renamed constant cannot
silently keep its real value. Without --timing, project runs with its own table.
Each test passes the factor or table it names; no one factor serves every test
(R-29).

This process is project's own: its pid, process group, signal handlers, streams
and exit status are the ones `python3 project ARGS...` would have. project is
loaded as the module project_cli, registered in sys.modules before it executes
(a @dataclass under postponed annotations fails without it), and its __name__ is
not "__main__", so its own guard does not run the CLI. sys.argv and sys.path[0]
are set as `python3 project` has them: argparse's prog and workbenches()' marker
read sys.argv[0].

Pitfalls the harness spike proved: a default argument or a constant derived from
TIMING at import keeps its old value when the table is replaced, so project reads
TIMING[...] when called; and a DeprecationWarning prints in a plain run but not
under this launcher, so project calls nothing deprecated (observed_at comes from
time.gmtime(), not datetime.utcnow()).

unittest discovery never imports this file (it takes test*.py); a test imports it
from tests/ as launch_project, or runs it as a script.
"""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "project"
MODULE_NAME = "project_cli"
PREFIX = "--timing="


def load(path=CLI, name=MODULE_NAME):
    """project as a module, loaded as tests/test_project.py loads it and registered in
    sys.modules before it executes, since dataclasses look a class's module up there."""
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def timing_overrides(text):
    """The --timing object, checked: a JSON object whose values are numbers. Exits nonzero,
    naming the fault, otherwise."""
    try:
        value = json.loads(text)
    except ValueError as exc:
        sys.exit(f"launch_project: --timing is not JSON: {exc}")
    if not isinstance(value, dict):
        sys.exit("launch_project: --timing must be a JSON object of TIMING keys")
    wrong = sorted(key for key, number in value.items()
                   if isinstance(number, bool) or not isinstance(number, (int, float)))
    if wrong:
        sys.exit(f"launch_project: TIMING values must be numbers: {', '.join(wrong)}")
    return value


def prepare(argv):
    """Load project and, when argv starts with --timing=JSON, replace its TIMING with a new
    dict: the real table updated by the object's values as floats. Returns the module and
    the remaining arguments. Changes neither sys.argv nor sys.path."""
    rest = list(argv)
    overrides = None
    if rest and rest[0].startswith(PREFIX):
        overrides = timing_overrides(rest.pop(0)[len(PREFIX):])
    module = load()
    if overrides is not None:
        unknown = sorted(set(overrides) - set(module.TIMING))
        if unknown:
            sys.exit(f"launch_project: unknown TIMING keys: {', '.join(unknown)}")
        module.TIMING = {**module.TIMING, **{key: float(value) for key, value in overrides.items()}}
    return module, rest


def main(argv):
    """Run project's main() with the remaining arguments, as `python3 project` would."""
    module, rest = prepare(argv)
    sys.argv = [str(CLI), *rest]
    sys.path[0] = str(ROOT)
    return module.main(rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
