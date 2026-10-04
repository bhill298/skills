---
name: prompt-research-existing
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Research the existing options for the specified goal. Compare capability, maturity, maintenance, user feedback, setup effort, and fit with the user's environment. Use current documentation and practical evidence; treat popularity as one signal. Explain what each option would give the user, its important limitations, and what you recommend. Identify existing tools we could reuse before proposing a new implementation.
