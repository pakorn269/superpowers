## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2026-03-21 - [Insecure Port Generation using Math.random()]
**Vulnerability:** The brainstorming server generated its random port using `Math.random()`, which is cryptographically insecure.
**Learning:** `Math.random()` should never be used for security-sensitive logic like port selection, as it is predictable.
**Prevention:** Use `crypto.randomInt(min, max)` for generating secure random integers in Node.js.
