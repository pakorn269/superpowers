## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-18 - Replace string operations with slice for multi-megabyte HTML screens
**Learning:** In string replacements in V8 on multi-megabyte inputs, calling `String.prototype.replace()` incurs an immense penalty. Large allocations block the event loop and dramatically impact response times.
**Action:** Use `.indexOf()` or `.lastIndexOf()` to locate markers, and concatenate strings with `.slice()` to drastically reduce execution time (e.g. from 90ms to <0.1ms).
