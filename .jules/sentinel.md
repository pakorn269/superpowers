## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-03-01 - [Memory Exhaustion (DoS) in WebSocket Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` lacked bounds checking on incoming payloads and buffer accumulation, allowing a malicious client to exhaust memory by sending a continuously large payload or an incomplete frame with an artificially large length marker.
**Learning:** Custom protocol parsers (especially zero-dependency ones) must explicitly enforce maximum size limits on buffers and payloads because default network buffers are only bounded by available system memory, creating a significant Denial of Service (DoS) risk.
**Prevention:** Always implement explicit maximum payload constraints (e.g., 10MB) during frame decoding (`decodeFrame`) and enforce limits on accumulated buffers in data event handlers (`socket.on('data')`) to immediately terminate non-compliant connections.
