---
name: prompt-save-handoff
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Update the appropriate project notes so a fresh session can continue without repeating investigation or settled decisions. Record the objective, agreed constraints, current implementation, relevant files and commands, completed verification, unresolved questions, and next steps. Distinguish confirmed facts from assumptions. Consolidate existing notes where possible and remove stale guidance.
