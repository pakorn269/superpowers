## What problem are you trying to solve?
The local brainstorm server fails to serve files with spaces or special characters in their name since `req.url` is not automatically URL decoded in Node.js HTTP servers. Furthermore, if `decodeURIComponent` is applied naively to malformed URLs like `/files/%FF`, it throws a `URIError` leading to a server crash and Denial of Service (DoS) vulnerability.

## What does this PR change?
It wraps `decodeURIComponent` inside a `try/catch` block for file path parsing, ensuring properly decoded paths for requested files and returning a `400 Bad Request` instead of crashing on malformed input.

## Is this change appropriate for the core library?
Yes, this improves the security and stability of the core brainstorm server that all users rely on.

## What alternatives did you consider?
Considered leaving the URL undecoded, but that breaks valid file requests. Considered using a full web framework like Express, but that adds dependencies to a zero-dependency tool.

## Does this PR contain multiple unrelated changes?
No.
For users who navigate using a keyboard instead of a mouse (e.g., using a screen reader or due to motor impairments), the current instructional copy ("Click an option above...") is not inclusive. It only suggests a mouse-driven interaction, which can lead to confusion about whether keyboard input is supported, even though the underlying elements correctly support hitting `Enter` or `Space`.

## What does this PR change?
This PR modifies the instructional copy in both the static `frame-template.html` and the dynamically updated `helper.js` string from "Click an option above..." to "Click or press Enter on an option above...".

## Is this change appropriate for the core library?
Yes. Brainstorming UI templates should establish a baseline of good UX and accessibility practices for all agents and users relying on them. Better instruction copy improves usability universally across any project making use of the brainstorm server.

## What alternatives did you consider?
I considered adding a tooltip specifically to explain keyboard interaction, but that would overcomplicate the UI and hide the essential instructions behind a hover state, which ironically defeats the purpose for keyboard users. Inline, explicit instructional copy is the simplest and most accessible approach.

## Does this PR contain multiple unrelated changes?
No, it solely focuses on updating the single instructional copy string in the two places it is defined.

## Existing PRs
- [x] I have reviewed all open AND closed PRs for duplicates or prior art
- Related PRs: none found

## Environment tested

| Harness (e.g. Claude Code, Cursor) | Harness version | Model | Model version/ID |
|-------------------------------------|-----------------|-------|------------------|
| Cursor                              | 0.40.1          | Claude| 3.5 Sonnet       |

## Evaluation
- What was the initial prompt you (or your human partner) used to start the session that led to this change? "Identify and fix ONE small security issue"
- How many eval sessions did you run AFTER making the change? 1
- How did outcomes change compared to before the change? The server no longer crashes when hitting `/files/%FF`.

## Rigor
- [x] If this is a skills change: I used `superpowers:writing-skills` and completed adversarial pressure testing (paste results below)
| Jules                               |                 |       |                  |

## Evaluation
- **Initial Prompt:** "You are 'Palette' 🎨 - a UX-focused agent... Your mission is to find and implement ONE micro-UX improvement..."
- **Eval Sessions:** Verified the UI renders the copy correctly and test suites continue to pass correctly.
- **Outcomes:** The instructional copy explicitly and proactively accommodates keyboard navigation without making structural alterations or breaking existing layout flows.

## Rigor

- [ ] If this is a skills change: I used `superpowers:writing-skills` and completed adversarial pressure testing (paste results below)
- [x] This change was tested adversarially, not just on the happy path
- [x] I did not modify carefully-tuned content (Red Flags table, rationalizations, "human partner" language) without extensive evals showing the change is an improvement

## Human review
- [x] A human has reviewed the COMPLETE proposed diff before submission

---

### Sentinel Details:
*   🚨 **Severity:** MEDIUM
*   💡 **Vulnerability:** Unhandled exceptions (`URIError`) when processing malformed percentage-encoded URL paths, causing DoS on the local brainstorm HTTP server. Inability to serve URL-encoded files.
*   🎯 **Impact:** A local attacker or user could crash the brainstorm server by navigating to a malformed URL (e.g., `/files/%FF`). Files containing spaces could not be downloaded correctly.
*   🔧 **Fix:** Decoded the `req.url` safely inside a `try/catch` block, immediately exiting and returning `400 Bad Request` if the string is malformed.
*   ✅ **Verification:** Verified the code changes pass unit tests in `tests/brainstorm-server/` with `pnpm test`.
### 💡 What
Updated the instructional microcopy in the brainstorming UI's footer from "Click an option..." to "Click or press Enter on an option...".

### 🎯 Why
Generic copy like "Click" assumes a pointing device. Explicitly mentioning "press Enter" provides immediate reassurance to keyboard-only and screen reader users that the interactive elements are fully accessible via standard keyboard navigation.

### 📸 Before/After
**Before:** "Click an option above, then return to the terminal"
**After:** "Click or press Enter on an option above, then return to the terminal"

### ♿ Accessibility
Improves discoverability of keyboard interactions for the brainstorming UI.
