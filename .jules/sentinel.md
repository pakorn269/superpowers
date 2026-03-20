## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-02-15 - [Unbounded WebSocket Buffer DoS in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` appended incoming chunks to a buffer without any size limits, allowing an attacker to send an infinitely large frame (or just raw data) causing memory exhaustion (Denial of Service).
**Learning:** Custom stream-based protocol parsers like WebSockets must enforce explicit maximum payload/buffer size limits to prevent out-of-memory crashes when parsing maliciously crafted large frames.
**Prevention:** Enforce a maximum buffer size limit (e.g., 10MB) after attempting to process valid frames from the buffer, closing the connection if the limit is exceeded.
