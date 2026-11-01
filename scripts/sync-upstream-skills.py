"""Vendor selected skill folders from a pinned GitHub archive (Python 3.9+)."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "upstream" / "sources.json"


def digest(data):
    # Git may convert text line endings on checkout.
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def local_path(relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or "\\" in relative or ":" in relative:
        raise ValueError(f"Unsafe path: {relative}")
    target = ROOT.joinpath(*path.parts)
    if not target.resolve().is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {relative}")
    for parent in (target, *target.parents):
        if parent == ROOT:
            break
        if parent.is_symlink() or getattr(parent, "is_junction", lambda: False)():
            raise ValueError(f"Linked destination: {relative}")
    return target


def sync(commit=None):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    commit = commit or manifest["commit"]
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Use a full, lowercase 40-character commit SHA.")
    repo = manifest["repository"]
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo):
        raise ValueError("Invalid GitHub repository.")

    mappings = manifest["skills"]
    destinations = list(mappings.values())
    license_path = manifest["license"]
    for index, destination in enumerate(destinations):
        local_path(destination)
        if not destination.startswith("skills/"):
            raise ValueError("Skill destinations must be inside skills/.")
        for other in destinations[index + 1:]:
            if destination == other or destination.startswith(other + "/") or other.startswith(destination + "/"):
                raise ValueError("Skill destinations overlap.")
    if not license_path.startswith("upstream/") or license_path == "upstream/sources.json":
        raise ValueError("License must be a separate file inside upstream/.")
    local_path(license_path)

    def managed(name):
        return name == license_path or any(name.startswith(d + "/") for d in destinations)

    previous = manifest["files"]
    for name, expected in previous.items():
        if not managed(name):
            raise ValueError(f"Manifest tracks a file outside the selected destinations: {name}")
        path = local_path(name)
        if not path.is_file() or digest(path.read_bytes()) != expected:
            raise ValueError(f"Local change detected: {name}. Preserve or revert it before syncing.")
    for destination in destinations:
        directory = local_path(destination)
        if directory.exists():
            if not directory.is_dir():
                raise ValueError(f"Destination is not a directory: {destination}")
            for path in directory.rglob("*"):
                name = path.relative_to(ROOT).as_posix()
                local_path(name)
                if path.is_file() and name not in previous:
                    raise ValueError(f"Untracked local file in imported folder: {name}")
    if local_path(license_path).exists() and license_path not in previous:
        raise ValueError(f"Untracked license destination: {license_path}")

    url = f"https://codeload.github.com/{repo}/zip/{commit}"
    print(f"Downloading {repo}@{commit}")
    request = urllib.request.Request(url, headers={"User-Agent": "skills-vendor-sync"})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive_bytes = response.read()
    incoming = {}
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        for member in archive.infolist():
            if member.is_dir():
                continue
            parts = member.filename.split("/", 1)
            if len(parts) != 2:
                continue
            source = parts[1]
            destination = license_path if source == "LICENSE" else None
            for prefix, target in mappings.items():
                if source.startswith(prefix + "/"):
                    destination = target + source[len(prefix):]
                    break
            if destination is None:
                continue
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"Upstream symlink requires review: {source}")
            local_path(destination)
            if destination in incoming:
                raise ValueError(f"Duplicate archive destination: {destination}")
            incoming[destination] = archive.read(member)
    for destination in destinations:
        if destination + "/SKILL.md" not in incoming:
            raise ValueError(f"Missing SKILL.md in archive: {destination}")
    if license_path not in incoming:
        raise ValueError("Missing upstream LICENSE.")

    # Validate the complete import before changing any repository files.
    for name, data in incoming.items():
        path = local_path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists() or digest(path.read_bytes()) != digest(data):
            path.write_bytes(data)
    for name in previous.keys() - incoming.keys():
        local_path(name).unlink()
    manifest["commit"] = commit
    manifest["files"] = {name: digest(data) for name, data in sorted(incoming.items())}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {len(destinations)} skills and license ({len(incoming)} files). Review git diff before committing.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", help="Update to a full upstream commit SHA; defaults to the pinned SHA.")
    args = parser.parse_args()
    try:
        sync(args.commit)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Sync failed: {error}\n")
