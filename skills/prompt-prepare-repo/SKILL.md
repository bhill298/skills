---
name: prompt-prepare-repo
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Check that someone starting from a fresh checkout can reproduce this workflow using the repository and documented downloads. Fix missing instructions, dependencies, paths, and setup steps. Keep reusable tooling separate from individual runs and generated artifacts. Update README and relevant agent instructions to match the actual behavior. Check repository hygiene without adding unnecessary audit tooling. Report anything that still depends on undocumented local state.
