# Manual invocation across harnesses

Verified against official documentation on 2026-09-28. Recheck relevant documentation if a target version behaves differently.

| Harness | Mechanical control | Invocation |
| --- | --- | --- |
| Codex | `agents/openai.yaml`: `policy.allow_implicit_invocation: false` | `$name input` |
| Claude Code | `SKILL.md`: `disable-model-invocation: true` | `/name input` |
| Pi | `SKILL.md`: `disable-model-invocation: true` | `/skill:name input` |
| OpenCode v2 | `SKILL.md`: `metadata.opencode/autoinvoke: false` | Native skill selection by ID in the target UI |
| OpenCode v1 | Exact-name skill denial in settings, or exclusion from discovery plus a command adapter | Native invocation where verified, or `/name input` through an adapter |

All three controls can coexist. OpenCode v1 ignores the OpenCode metadata flag as well as the other harnesses' controls. A sentence in a description or body is an instruction, not mechanical exclusion.

## OpenCode v2

Include the following in every generated skill's frontmatter, alongside `disable-model-invocation: true`:

```yaml
metadata:
  opencode/autoinvoke: false
```

This omits the skill from the model's available list while leaving it registered and explicitly loadable by ID. It does not prohibit a skill-tool call when the ID is already known. Keep the body instruction requiring explicit user invocation. Do not set `slash: false` or `metadata.opencode/slash: false`, which would hide interactive discovery.

Use a normal discovered skills directory; shared `~/.agents/skills/` or project `.agents/skills/` is suitable for Codex/OpenCode v2 use. No permission denial or command wrapper is required for this control. Verify the target UI's native invocation syntax before reporting an example. Keep an existing command adapter if it is still useful or supports v1.

## OpenCode v1 settings and adapter

For v1, storing the canonical skill outside OpenCode's discovered skill directories avoids a settings change. For a Codex/OpenCode installation, `~/.codex/skills/<name>/` works with documented default discovery: Codex loads it, and an OpenCode command can read it explicitly. Check custom `skills.paths` settings before relying on exclusion.

OpenCode discovers `.opencode/skills`, `.claude/skills`, and `.agents/skills`, plus their documented global equivalents, including `~/.config/opencode/skills`. If the canonical skill is in any discovered path, merge an exact-name denial into the effective OpenCode configuration, preserving existing JSON/JSONC and rule precedence:

```json
{
  "permission": {
    "skill": {
      "chosen-name": "deny"
    }
  }
}
```

This hides the skill and rejects loading it through the skill tool. Verify whether native user invocation in the installed v1 version still loads it; if so, no adapter is needed. Otherwise use the adapter below, which reads the canonical file as a normal file rather than calling the denied skill tool. Do not deny file reading, disable all skills, or add a blanket permission change. If an existing configuration cannot be safely merged, explain what remains unconfigured rather than claiming manual-only enforcement. Do not apply this v1 configuration schema to v2.

Create `~/.config/opencode/commands/<name>.md` for personal use or `.opencode/commands/<name>.md` for project use, respecting a configured alternate config location:

```markdown
---
description: Manual prompt.
---

The user explicitly invoked this prompt command. Read the canonical skill at `RESOLVED_SKILL_PATH` and perform its instructions now. Use the accompanying input below as the invocation text. Resolve supporting files relative to the canonical skill directory.

Input:
$ARGUMENTS
```

Replace `RESOLVED_SKILL_PATH` with the actual path; leave `$ARGUMENTS` literal in the command file. Use forward slashes for Windows paths. For a portable project installation, identify the path relative to the project root. The native command substitutes its arguments, and the agent loads the one canonical prompt. Verify that the command exists and its target resolves. Do not overwrite an unrelated command with the same name.

If OpenCode is the only target, the canonical skill may live in a dedicated directory outside skill discovery, such as `~/.config/opencode/prompt-templates/<name>/`, with the same command adapter. The creator itself can use this adapter too.

## Argument behavior and discovery

Codex receives the user's accompanying message alongside the explicitly loaded skill; do not promise Pi-style macro expansion in a Codex skill. Claude Code appends supplied arguments when the skill does not contain argument placeholders. Pi appends text after `/skill:name` as a user request. The shared body therefore needs no argument macro.

Shared `.agents/skills/` discovery works in Codex, OpenCode, and Pi; it does not establish a universal manual-only policy. Claude Code has its own documented personal/project skill locations. Install or link the canonical folder into a harness's supported location only when needed, accounting for OpenCode discovery before using a shared location.

## Sources

- [Codex skills](https://learn.chatgpt.com/docs/build-skills) and [Codex prompt deprecation](https://learn.chatgpt.com/docs/custom-prompts).
- Codex's bundled `skill-creator/references/openai_yaml.md` documents `policy.allow_implicit_invocation` and explicit `$skill` invocation.
- [Claude Code skills](https://code.claude.com/docs/en/skills): manual-only invocation and appended arguments.
- [Pi skills](https://pi.dev/docs/latest/skills): manual-only invocation, arguments, and shared directories.
- [OpenCode v2 skills](https://opencode.ai/v2/docs/skills): `metadata.opencode/autoinvoke`, discovery, and explicit loading.
- [OpenCode v1 skills](https://opencode.ai/docs/skills/): discovery, ignored frontmatter fields, and exact-name permissions.
- [OpenCode commands](https://opencode.ai/docs/commands/): command directories and argument substitution.
