## 2026-03-14 - Optimize isFullDocument string allocation
**Learning:** Brainstorm server receives full HTML screens that can be multi-megabytes. Calling `toLowerCase()` on the entire string before checking the first few characters for `<!doctype` causes huge unnecessary memory allocations and blocks the event loop.
**Action:** Only substring the first few characters (e.g., 20) of large text payloads before calling string transformation functions like `toLowerCase()` when doing prefix checks.

## 2026-03-24 - Avoid String.prototype.replace() on multi-megabyte strings
**Learning:** Using `String.prototype.replace()` (even with a simple string pattern) on multi-megabyte HTML payloads causes massive event-loop blocking overhead (~27ms for a 5MB string vs ~0.03ms with slice). This affects both `wrapInFrame` (replacing `<!-- CONTENT -->`) and `handleRequest` (injecting before `</body>`).
**Action:** Always prefer `indexOf`/`lastIndexOf` combined with `String.slice()` for inserting or replacing content in large string payloads.

## 2026-03-25 - Avoid String.prototype.trimStart() on multi-megabyte strings
**Learning:** Calling `trimStart()` on a multi-megabyte string (e.g., large HTML screens in brainstorm-server) before applying prefix substring operations forces an expensive, complete copy of the string in memory. This blocks the event loop significantly (e.g., ~5-18ms for 5MB) compared to direct regex prefix tests (~0.28ms).
**Action:** Always prefer a bounded regex check like `/^\s*(?:<!doctype|<html)/i.test(html)` over unbounded full-string trim operations when checking prefixes of large payloads.

## 2026-03-25 - Async directory read in server startup
**Learning:** `fs.promises.readdir` has slightly higher overhead than `fs.readdirSync` for small directories, but async startup is preferred in server contexts to avoid blocking the event loop during initialization.
**Action:** Use `fs.promises.mkdir` and `fs.promises.readdir` in `startServer` (now async), even for one-time startup I/O, to keep startup non-blocking and consistent with other async I/O in the codebase.

## 2026-04-12 - Precalculate string slices for template injection
**Learning:** Dynamically calling `indexOf` and `slice` on a large static template string (like `frame-template.html`) for every incoming request introduces unnecessary overhead (e.g. ~0.7ms vs ~0.17ms for wrapping 5MB content), even when bypassing `replace()`.
**Action:** If the template and target insertion marker are static, precalculate and store the `start` and `end` slices at startup. Then, simply concatenate the precalculated chunks around the dynamic payload during requests.

## 2026-03-26 - Avoid full-string regex matches in large files
**Learning:** Using a regular expression like `/^---\n([\s\S]*?)\n---\n([\s\S]*)$/` to extract frontmatter from potentially large markdown files causes massive string allocation and high regex engine execution overhead because it captures the entire file body.
**Action:** When extracting short chunks from the beginning of large files, use string primitives like `indexOf` and `slice` instead of regular expressions that match the entire remaining content.

## 2026-03-27 - Async file stat reads
**Learning:** `fs.statSync` and `fs.readdirSync` inside `getNewestScreen` block the event loop for every incoming request. Also, executing `Promise.all` on `fs.promises.stat` across a large directory can trigger `EMFILE` errors.
**Action:** Process async file operations sequentially with a `for...of` loop and `fs.promises.stat` to maintain an unblocked event loop and prevent hitting open file limits.

## 2026-04-14 - Avoid per-request filesystem I/O in route handlers
**Learning:** Calling `fs.promises.readdir` and `fs.promises.stat` inside the root HTTP handler (`GET /`) executes disk I/O on every single request. Even when using async variants, this creates a major performance bottleneck under load compared to serving from memory.
**Action:** When serving static files that are already being monitored by `fs.watch`, maintain a cached state (e.g., `cachedNewestScreen`) in memory. Update the cache on startup and inside the watcher callback, and serve requests directly from the memory cache.
## 2026-04-09 - Avoid string replace on multi-megabyte HTML screens
**Learning:** Using `String.prototype.replace()` on multi-megabyte HTML strings (e.g., when injecting helpers before `</body>`) forces the regex engine or string scanner to traverse the entire string from the beginning, blocking the event loop for a significant amount of time (~27ms for 5MB).
**Action:** Use `String.prototype.lastIndexOf()` combined with string `slice()` when inserting content near the end of massive strings, which operates almost instantly (~0.03ms).
## 2026-04-14 - Avoid per-request filesystem I/O in route handlers
**Learning:** Calling `fs.promises.readdir` and `fs.promises.stat` or even `fs.promises.readFile` inside the root HTTP handler (`GET /`) executes disk I/O on every single request. This creates a major performance bottleneck under load compared to serving from memory. Moreover, string manipulation inside the route handler also impacts the event loop negatively.
**Action:** When serving static files or fully constructed string responses that are already being monitored by `fs.watch`, maintain a cached string state (e.g., `cachedHtmlResponse`) in memory. Update the cache on startup and inside the watcher callback, and serve requests directly from the memory cache.
## 2026-04-16 - Eliminate filesystem I/O and repetitive string manipulation in frequent route handlers
**Learning:** In Node.js server scripts, avoid performing filesystem I/O (e.g., `readFile`) or repetitive string manipulation inside frequently accessed route handlers (e.g., `GET /`). This introduces severe bottlenecks and overhead per-request.
**Action:** Instead, cache the fully constructed response globally and update it on startup and via `fs.watch` callbacks to eliminate the read and allocation overhead on every request.
## 2026-04-14 - Await inside handleRequest
**Learning:** Refactoring a synchronous function to `async` without properly updating its call sites introduces bugs. For example, the `await` was added in `handleRequest` without making the function async, which broke parsing. Once fixed, the server operates correctly.
**Action:** When making route handlers async, thoroughly verify and update all internal logic to handle `await` results to prevent syntax or runtime regressions.

## 2026-04-14 - Avoid per-request filesystem I/O in route handlers
**Learning:** Calling `fs.promises.readdir` and `fs.promises.stat` inside the root HTTP handler (`GET /`) executes disk I/O on every single request. Even when using async variants, this creates a major performance bottleneck under load compared to serving from memory. Moreover, reading and wrapping the file in HTML templates dynamically for every single request duplicates effort unnecessarily.
**Action:** When serving static files that are already being monitored by `fs.watch`, maintain a fully constructed `cachedHtml` state in memory. Update the cache on startup and inside the watcher callback, and serve requests directly from the memory cache.
