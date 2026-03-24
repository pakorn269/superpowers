## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-03-24 - [Unbounded WebSocket Buffer Size (DoS)]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` was continuously appending incoming chunks to a buffer (`buffer = Buffer.concat([buffer, chunk])`) without enforcing a maximum limit. An attacker or malfunctioning client could stream unbounded un-framed data (where `decodeFrame` fails to consume bytes), resulting in memory exhaustion and Denial of Service (OOM).
**Learning:** In stream-based protocol parsers (like custom WebSockets without external dependencies), continuously growing buffers are a severe DoS vector if limit checks are absent. Buffer sizes must be explicitly capped.
**Prevention:** Always enforce a strict memory limit on incoming buffers (e.g., 10MB) immediately after reading and parsing chunks in the `socket.on('data')` handler. If the limit is exceeded, forcefully terminate the connection with `socket.destroy()`.
