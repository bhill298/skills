---
name: prompt-verify-work
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Determine and run the most useful verification you can perform independently for this work. Exercise the actual user-facing entry points and important state transitions. Where live testing is unavailable, use a realistic simulation grounded in the source, schema, or captured behavior. Add regression coverage for meaningful failures uncovered. Clearly distinguish what was verified live, simulated, or remains unverified.
