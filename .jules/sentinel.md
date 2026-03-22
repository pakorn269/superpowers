## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-02-15 - [Unbounded Buffer Memory Exhaustion (DoS) in Custom WebSocket Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` appended incoming data chunks to a buffer without any size limits. An attacker could send a continuous stream of incomplete frames, causing the server to allocate memory until it crashes (DoS).
**Learning:** Custom stream parsers (like zero-dependency WebSockets) must enforce explicit maximum payload/buffer size limits (e.g., 10MB) in data handlers to prevent memory exhaustion attacks.
**Prevention:** Always place a buffer length check (e.g., `if (buffer.length > MAX_BUFFER_SIZE) { socket.destroy(); }`) *after* extracting valid frames from the buffer to avoid falsely triggering the limit on legitimate chunks that happen to contain multiple valid frames.
