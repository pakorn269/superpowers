## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2024-05-18 - Avoid String.prototype.replace with function replacer on massive strings
**Learning:** Using `String.prototype.replace(target, () => content)` on large, multi-megabyte strings (like full HTML screens in brainstorm-server) causes a massive performance overhead and blocks the event loop (~171ms vs ~1ms for a 10MB string).
**Action:** Prefer using `lastIndexOf` or `indexOf` combined with `slice()` for injecting content into multi-megabyte strings to avoid huge string replacement penalties.
