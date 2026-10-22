#!/usr/bin/env bash
# qs.sh: run one check of this feature's quickstart.md as one command, with no shell state from the caller.
#
# Usage: bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id> [NAME=VALUE ...]
#
# It works from anywhere in the work tree: it changes to the top of the work tree first, so a path given in
# a NAME=VALUE is read from there (give an absolute path, or one relative to the top of the work tree).
# It takes the fenced block of the quickstart.md in this script's own directory whose first line is exactly
# "# check: <check-id>", exports BASE and every NAME=VALUE, runs the block with bash and exits with the
# block's own status. BASE is "git merge-base origin/main HEAD" unless the call passes BASE=<sha>; a BASE
# left in the caller's environment is ignored. Exit 2 means the runner could not run the check (bad
# arguments, no such block, or the marker found on more than one block); any other status is the block's.
# Outside a git work tree it stays in the current directory (a plain scratch copy: run it from the copy's
# top and pass BASE=<sha>). Inside one, the script must be the work tree's own copy.
# No network is used.
set -u

die() { printf 'qs.sh: %s\n' "$*" >&2; exit 2; }

[ "$#" -ge 1 ] || die "usage: bash specs/006-refuse-non-directory-parent-early/qs.sh <check-id> [NAME=VALUE ...]"
ID=$1; shift
case $ID in
  "" | *[!A-Za-z0-9._-]*) die "bad check id '$ID'" ;;
esac
unset BASE
for ARG in "$@"; do
  case $ARG in
    [A-Za-z_]*=*) ;;
    *) die "bad argument '$ARG'; expected NAME=VALUE" ;;
  esac
  case ${ARG%%=*} in
    *[!A-Za-z0-9_]*) die "bad variable name in '$ARG'; expected NAME=VALUE" ;;
  esac
done

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P) || die "cannot find this script's directory"
QS=$HERE/quickstart.md
[ -f "$QS" ] || die "no quickstart.md next to this script ($QS)"
ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || ROOT=
if [ -n "$ROOT" ]; then
  [ "$HERE" = "$ROOT/specs/006-refuse-non-directory-parent-early" ] \
    || die "this script is in $HERE, not in the work tree at $ROOT; run it from the work tree that holds it"
else
  ROOT=$(pwd -P)
fi
cd "$ROOT" || die "cannot change to $ROOT"

for ARG in "$@"; do export "$ARG"; done
if [ -z "${BASE:-}" ]; then
  BASE=$(git merge-base origin/main HEAD 2>/dev/null) && [ -n "$BASE" ] \
    || die "cannot compute BASE (git merge-base origin/main HEAD failed); pass BASE=<sha>"
fi
export BASE

# One pass: the number of blocks that start with the marker, then the text of the block(s).
OUT=$(awk -v id="$ID" '
  /^ *```/ { if (inb) { inb = 0; grab = 0 } else { inb = 1; first = 1 }; next }
  inb && first { first = 0; if ($0 == "# check: " id) { grab = 1; n++ } }
  grab { buf = buf $0 "\n" }
  END { print n + 0; printf "%s", buf }' "$QS") || die "cannot read $QS"
N=${OUT%%$'\n'*}
BLOCK=${OUT#*$'\n'}
case $N in
  1) ;;
  0) die "no block of $QS starts with '# check: $ID'" ;;
  *) die "'# check: $ID' starts $N blocks of $QS; it must start exactly one" ;;
esac

printf 'qs.sh: check %s at BASE %s in %s\n' "$ID" "$BASE" "$ROOT" >&2
exec bash -c "$BLOCK" "qs.sh:$ID"
