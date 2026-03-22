## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-22 - Optimize String Replacement for Large Payloads
**Learning:** `String.prototype.replace()` incurs massive overhead on multi-megabyte strings (like HTML payloads), even when doing simple literal replacements.
**Action:** Prefer `lastIndexOf` or `indexOf` combined with string `slice()` for injecting strings into large text payloads.
