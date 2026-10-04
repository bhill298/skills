---
name: prompt-review-code
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Review the specified code or changes. Verify that the implementation does what it claims and meets the intended requirements. Identify concrete bugs, regressions, limitations, and meaningful tradeoffs. Explain the practical impact and support findings with code references. Recommend improvements that add real value; avoid changes for their own sake.
