## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-14 - Optimize helper injection into large HTML strings
**Learning:** `String.prototype.replace()` incurs massive performance overhead when operating on multi-megabyte strings, like full HTML screens generated in the brainstorming server. The regex engine or matching logic scales poorly for huge strings.
**Action:** When modifying large multi-megabyte strings, always prefer using `lastIndexOf` or `indexOf` combined with `String.prototype.slice()` rather than `String.prototype.replace()`.
