# Skills

Personal agent skills and selected skills vendored from upstream projects.

## Clone

```sh
git clone https://github.com/bhill298/skills.git
cd skills
```

Everything is included in a normal clone, including the upstream skills and their
supporting files. No submodules, symlinks, or post-clone downloads are required.
Use `git pull` to receive updates committed to this repository. Cloning does not
automatically install the skills into an agent application.

## Install Superpowers skills

Use [bhill298/superpowers-lite](https://github.com/bhill298/superpowers-lite)
to install Superpowers skills. It is maintained separately and is not vendored
in this repository. Follow its
[installation instructions](https://github.com/bhill298/superpowers-lite#install)
for supported agents, options, updates, and removal.

For example, with Python 3.11+ installed, clone it into a separate directory and
preview a Codex installation before applying it:

```sh
git clone https://github.com/bhill298/superpowers-lite.git
cd superpowers-lite
python superpowers-lite.py --only codex --dry-run
python superpowers-lite.py --only codex
```

Run these commands from outside this repository to keep the checkouts separate.
Use `python3` where appropriate, and restart affected agent sessions afterward.

## Vendored skills

The following folders under `skills/` come from
[mattpocock/skills](https://github.com/mattpocock/skills):

- `domain-modeling`
- `grill-with-docs`
- `grilling`
- `handoff`
- `teach`
- `wait-what`

Complete skill folders are imported without content changes. Their upstream
commit, source paths, destination paths, and file hashes are recorded in
[`upstream/sources.json`](upstream/sources.json). The upstream MIT license is
preserved in [`upstream/mattpocock-LICENSE`](upstream/mattpocock-LICENSE).

These are upstream instructions, including references to a tool named `Skill` in
`grill-with-docs` and `handoff`. Compatibility with a particular agent's skill
invocation mechanism may require adaptation; vendoring does not translate them.

### Dependency audit

At the initially audited revision (`4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`),
the selected set contained all named skill dependencies and bundled file references:

| Skill | Dependencies and workspace references |
| --- | --- |
| `domain-modeling` | Included `GLOSSARY-FORMAT.md` and `ADR-FORMAT.md`; creates glossary and ADR files in the working project as needed. |
| `grill-with-docs` | Invokes `grilling` and `domain-modeling`, both included. |
| `grilling` | No other skills or bundled files referenced; requests subagent support for fact-finding. |
| `handoff` | No fixed skill dependencies; writes a handoff to the OS temporary directory and suggests skills relevant to that session. |
| `teach` | All four format documents are included; mission, resources, lessons, assets, notes, and learning records belong to the teaching workspace. |
| `wait-what` | Uses the working project's glossary and optional glossary map; these are project context, not omitted upstream files. References ASD-STE100 as a writing convention, not a bundled document. |

All six folders also include their upstream `agents/openai.yaml` files. This is a
file/dependency audit, not an end-to-end runtime test in every agent application.
Recheck dependencies when updating the upstream revision. Use a separate teaching
workspace when its glossary should be distinct from a software project's glossary.

## Refresh upstream skills

Maintainers need Python 3.9+ and network access; no third-party Python packages
are required. Run from the repository root (use `python3` if appropriate):

```sh
# Fetch the latest files from the upstream repository's default branch:
python scripts/sync-upstream-skills.py

# Optional: import a specific revision instead (replace the placeholder):
python scripts/sync-upstream-skills.py --commit FULL_40_CHARACTER_COMMIT_SHA

git diff --check
git diff
```

The script discovers the upstream default branch (normally `main`) on each run,
resolves its current tip, and downloads that revision's archive. It copies only
the selected folders and license into this repository. The manifest's commit is
provenance for the last changed import, not a pin controlling future updates.
If those files are unchanged, nothing is written, even if upstream has new commits.
For manual updates, review and commit the imported files and manifest together.
Future clones receive those committed files.

### Automatic updates

[Sync upstream skills](.github/workflows/sync-upstream-skills.yml) runs weekly at
Friday 08:23 UTC and can also be started from GitHub's Actions tab. It runs the regression
tests, syncs upstream, and commits and pushes changed imports directly to this
repository's default branch (`main`). It does not open a PR. Changes to other
upstream files do not produce a commit here; imported additions, edits, deletions,
or license changes do. The recorded SHA changes only with an actual import change.

The workflow starts operating once it is pushed to the default branch with GitHub
Actions enabled. It uses the built-in `GITHUB_TOKEN` with `contents: write`; no
personal token is needed. Repository rules must allow that token to push directly
to the default branch. A rejected push or a concurrent branch update fails the run
without force-pushing; the next scheduled run retries from a fresh checkout.
GitHub may delay scheduled runs and may disable schedules in public repositories
after 60 days without repository activity. Clones and local pulls need no hooks.

The script refuses to overwrite modified, missing, or extra local files in the
managed destinations. Hash comparisons tolerate Git's CRLF/LF checkout conversion.
Preserve or revert local edits before syncing. Keep customized skills in separate
folders outside the managed destinations so upstream refreshes cannot replace them.
To add another skill from the same upstream repository, add its source and
destination to the manifest's `skills` mapping, then run the script.

Run the sync script's offline regression tests with:

```sh
python -m unittest discover -s tests -v
```
