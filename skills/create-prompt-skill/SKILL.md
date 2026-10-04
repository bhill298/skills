---
name: create-prompt-skill
description: Manual prompt creator.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Create or update a reusable prompt skill from the user's supplied prompt and requirements now. Use the text accompanying this invocation as the creation request. Treat the supplied prompt as content to save; execute it only if the user separately asks to run it.

Run this creator only when the user explicitly invokes it or asks to use it. The same rule applies to every prompt skill it creates.

## Author the prompt skill

- Preserve the user's wording, constraints, and intended action. Make only the changes needed for reuse; do not add a workflow, persona, tests, or approval gates the user did not request.
- Prefix every generated skill name and directory with `prompt-` so prompt templates group together in skill listings. Infer a short lowercase, hyphenated base name when none is given; add the prefix only if it is absent (for example, `review-code` becomes `prompt-review-code`). Use lowercase letters, digits, and single hyphens, with at most 64 characters including the prefix and no leading, trailing, or repeated hyphens. Keep the frontmatter name and directory name identical. Ask for the reusable prompt if it is missing and cannot be recovered from the user's referenced context.
- Keep the description nonempty and terse: `Manual prompt.` is sufficient. A description is required by several harnesses; omitting it is not portable.
- Write the prompt as direct instructions to perform the requested action now. Include this compact invocation contract before the saved prompt, adapting only when necessary:

  > Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

- Incorporate the invocation text from the conversation or the harness's appended arguments. Do not require placeholder expansion in the shared skill body. If the source uses positional or named placeholders, express their mapping and defaults in plain language without changing their meaning. If exact text substitution is required, use a native command adapter and disclose that distinction.
- Keep the saved action in the body of `SKILL.md`. Do not merely print an expanded prompt or explain how to perform it when the generated skill is invoked.
- Add only these frontmatter fields by default:

  ```yaml
  ---
  name: prompt-chosen-name
  description: Manual prompt.
  disable-model-invocation: true
  metadata:
    opencode/autoinvoke: false
  ---
  ```

- Also create `agents/openai.yaml` with:

  ```yaml
  policy:
    allow_implicit_invocation: false
  ```

Include all three controls together: the policy file for Codex, `disable-model-invocation` for Claude Code/Pi, and `metadata.opencode/autoinvoke` for OpenCode v2. Do not set `user-invocable: false`: that disables the user's invocation in Claude Code. OpenCode v2's flag removes automatic advertising; the skill remains loadable by ID, so it is not an access-control denial.

## Save and integrate

Respect the requested destination and scope. Otherwise use a personal skill beside this creator when it lives in a discoverable skills directory. In Codex, prefer the configured Codex home `skills/` directory, falling back to `~/.codex/skills/`. For a requested project skill, use the project's supported skill directory. Inspect existing files before updating; preserve unrelated metadata and edits.

For OpenCode, or installation into a shared `.agents/skills/` or `.claude/skills/` directory that OpenCode discovers, read [references/harnesses.md](references/harnesses.md). Determine the target version. OpenCode v2 honors the metadata flag and needs no settings change or adapter for invocation control. OpenCode v1 ignores it: configure an exact-name skill denial, or exclude the skill from discovery and provide a command adapter. Do not claim the metadata flag protects v1.

Default to the current harness. Add adapters for other harnesses when requested. Keep one canonical prompt where practical; do not install a collection of duplicate skills or edit unrelated harness configuration.

## Verify and finish

Check valid YAML, matching `prompt-`-prefixed name/directory, nonempty terse description, all three invocation controls, and preservation of the supplied prompt. Use the full prefixed name in any adapters, permission entries, and invocation examples. Inspect how supplied arguments and an invocation with no arguments will be handled. Check changed lines for trailing whitespace. If a bundled validator rejects `disable-model-invocation` solely because its field allowlist is older, retain the documented field and report that validator limitation.

Report the saved path and an exact invocation example: in Codex, `$prompt-chosen-name work on this project`; in Claude Code, `/prompt-chosen-name work on this project`; in Pi, `/skill:prompt-chosen-name work on this project`. For OpenCode, use the target version's verified native skill invocation or `/prompt-chosen-name ...` when a command adapter is installed. Mention any unverified harness behavior or required reload. Do not execute the newly saved prompt as part of validation.
