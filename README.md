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

At the pinned revision, the selected set contains all named skill dependencies and
bundled file references:

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
# Reproduce the currently pinned import:
python scripts/sync-upstream-skills.py

# Update to a reviewed upstream revision (replace the placeholder):
python scripts/sync-upstream-skills.py --commit FULL_40_CHARACTER_COMMIT_SHA

git diff --check
git diff
```

Choose a full commit SHA from the upstream repository's commit history. The script
downloads that revision's archive and copies only the selected folders and license
into this repository. It also updates the manifest. Review and commit the skill,
license, and manifest changes together; future clones receive those exact files.

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
