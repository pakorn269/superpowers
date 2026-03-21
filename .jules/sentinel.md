## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-02-15 - [Unbounded WebSocket Buffer in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` lacked a maximum buffer size limit when reading incoming socket data. An attacker could stream endless data without valid frame boundaries, causing uncontrolled memory growth and leading to Denial of Service (OOM crash).
**Learning:** Custom stream parsers, particularly zero-dependency protocols like WebSockets, must always enforce explicit bounds. Limits must be checked *after* consuming valid data to ensure legitimate, fast-flowing data containing multiple valid frames isn't incorrectly flagged.
**Prevention:** Add a constant threshold like `MAX_BUFFER_SIZE = 10 * 1024 * 1024` and destroy the socket if `buffer.length` exceeds this value after the frame consumption loop.
