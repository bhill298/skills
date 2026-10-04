---
name: prompt-autonomous-dev
description: Manual prompt.
disable-model-invocation: true
metadata:
  opencode/autoinvoke: false
---

Run only when explicitly invoked by the user. Perform the task below now, using the text accompanying this invocation as its input, scope, and additional instructions. Follow explicit user changes to the saved defaults. If no input is supplied, use the current project and conversation where sufficient; ask only for essential missing information. Apply this prompt to this task, not as standing instructions for unrelated future requests.

Read the current project state, agreed plan, and latest test results or feedback. Complete the remaining implementation and repairs within the agreed scope, including all useful testing you can do yourself. Check related implementations for the same defects. Continue until the work is complete or further progress genuinely needs the user's input or manual testing. If manual testing remains, prepare as few test sessions as practical, with exact steps, expected results, and what information the user should report.
