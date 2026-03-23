## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-14 - Optimize string injection for huge payloads
**Learning:** Brainstorm server receives multi-megabyte HTML strings and uses `.includes` followed by `.replace` to inject a helper script. `.replace()` on multi-megabyte strings introduces massive performance overhead and blocks the event loop.
**Action:** When modifying multi-megabyte strings (like large HTML screens), prefer using `.lastIndexOf` or `.indexOf` combined with string `.slice()` rather than `String.prototype.replace()`.
