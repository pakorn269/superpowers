## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-21 - Async Startup in Brainstorm Server
**Learning:** Micro-benchmarks of Node.js filesystem operations show that `fs.promises.readdir` has higher overhead than `fs.readdirSync` for small directories (e.g., < 100 files, ~2ms vs ~0.1ms). However, asynchronous startup is preferred in server contexts to avoid blocking the event loop and to maintain consistency with other async I/O patterns in the codebase.
**Action:** Use `fs.promises` for directory initialization and reading in server startup, even if called only once, to ensure non-blocking behavior and better scalability as the directory grows.
