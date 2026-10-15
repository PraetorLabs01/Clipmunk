"""Publishes a new Clipmunk version that friends' apps pick up automatically.

    release.bat "What's new in this version"

Bumps the version (1.1.0 -> 1.2.0, or pass --version 2.0.0), builds the installer,
and uploads it as a GitHub release. Clipmunk on friends' PCs checks on startup.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
INIT = os.path.join(ROOT, "clipdrop", "__init__.py")
UPDATE = os.path.join(ROOT, "clipdrop", "update.py")


def gh():
    for p in (shutil.which("gh"), r"C:\Program Files\GitHub CLI\gh.exe"):
        if p and os.path.exists(p):
            return p
    sys.exit("GitHub CLI isn't installed: winget install GitHub.cli")


def run(*args, capture=False):
    r = subprocess.run(args, cwd=ROOT, text=True, capture_output=capture)
    if r.returncode != 0:
        sys.exit(f"Failed: {' '.join(args[:3])}…\n{(r.stderr or '') if capture else ''}")
    return (r.stdout or "").strip()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


PRIVATE = re.compile(r"discord(?:app)?\.com/api/webhooks/\d+/|gh[opsu]_[A-Za-z0-9]{20,}|github_pat_\w{20,}", re.I)


def private_bits(folder):
    """Releases are public: no webhook links or tokens anywhere in the build (versions 1.1-1.6 shipped
    the #media webhook in share.json)."""
    found = []
    if os.path.exists(os.path.join(folder, "share.json")):
        found.append("share.json (Discord channels)")
    for base, _, files in os.walk(folder):
        for name in files:
            p = os.path.join(base, name)
            if os.path.splitext(name)[1].lower() in (".json", ".txt", ".ini", ".cfg", ".py", ".toml", ".yaml", ".yml") \
                    and os.path.getsize(p) < 5_000_000:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    if PRIVATE.search(f.read()):
                        found.append(os.path.relpath(p, folder))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notes", nargs="?", default="")
    ap.add_argument("--version")
    ap.add_argument("--repo", help="owner/name of the GitHub repo for releases")
    a = ap.parse_args()

    g = gh()
    run(g, "auth", "status", capture=True)
    repo = a.repo or re.search(r'^REPO = "(.*)"', read(UPDATE), re.M).group(1)
    if not repo:
        sys.exit('No release repo set yet. Run once with --repo yourname/Clipmunk')
    run(g, "repo", "view", repo, "--json", "name", capture=True)
    # The release is tagged on the commit that's pushed, so everything in the build must be committed first.
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT,
                           capture_output=True, text=True).stdout.strip()
    if dirty:
        sys.exit("Commit your changes first - the release is tagged on the pushed commit:\n" + dirty)

    old = re.search(r'__version__ = "(.+)"', read(INIT)).group(1)
    if a.version:
        new = a.version
    else:
        major, minor, *_ = (int(x) for x in old.split("."))
        new = f"{major}.{minor + 1}.0"
    write(INIT, f'__version__ = "{new}"\n')
    write(UPDATE, re.sub(r'^REPO = ".*"', f'REPO = "{repo}"', read(UPDATE), flags=re.M))
    print(f"Releasing Clipmunk {new} to github.com/{repo}")

    if subprocess.run(["cmd", "/c", os.path.join(ROOT, "build.bat")], cwd=ROOT, stdin=subprocess.DEVNULL).returncode:
        write(INIT, f'__version__ = "{old}"\n')
        sys.exit("Build failed; version left at " + old)
    leaks = private_bits(os.path.join(ROOT, "release", "Clipmunk"))
    if leaks:
        sys.exit("Not released - the build contains private things:\n  " + "\n  ".join(leaks))
    missing = [f for f in ("LICENSE.txt", "THIRD-PARTY-NOTICES.txt")
               if not os.path.exists(os.path.join(ROOT, "release", "Clipmunk", f))]
    if missing:
        sys.exit("Not released - the build is missing " + ", ".join(missing))
    setup = os.path.join(ROOT, "Clipmunk-Setup.exe")
    with open(setup, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    # Commit and push the version bump first, then tag exactly that commit.
    run("git", "add", INIT, UPDATE)
    run("git", "commit", "-q", "-m", f"Release {new}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    run("git", "push", "-q", "origin", "HEAD:main")
    sha = run("git", "rev-parse", "HEAD", capture=True)
    notes = (a.notes or f"Clipmunk {new}") + f"\n\nSHA-256 of Clipmunk-Setup.exe: `{sha256}`"
    run(g, "release", "create", f"v{new}", setup, "--repo", repo, "--target", sha, "--title", f"Clipmunk {new}",
        "--notes", notes)
    print(f"\nDone. Friends will see 'Update to {new}' next time they open Clipmunk.")
    print(f"First-time download link: https://github.com/{repo}/releases/latest/download/Clipmunk-Setup.exe")


if __name__ == "__main__":
    main()
