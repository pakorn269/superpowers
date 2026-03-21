## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-21 - Avoid String.prototype.replace() for massive strings
**Learning:** Using `String.prototype.replace()` on multi-megabyte strings (like full HTML screens in brainstorm-server) causes enormous performance overhead and blocks the event loop.
**Action:** Use `lastIndexOf()` or `indexOf()` combined with `String.slice()` instead of `replace()` when modifying massive strings.
