## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.
## 2024-05-20 - [Unbounded WebSocket Buffer DoS Risk]
**Vulnerability:** The custom WebSocket server (`skills/brainstorming/scripts/server.js`) was missing an explicit maximum size limit when accumulating incoming data chunks into its `buffer` during the `socket.on('data')` event.
**Learning:** Custom stream-based protocol parsers are susceptible to unbounded memory exhaustion attacks (DoS) when attackers send continuous streams of incomplete frames or excessively large payloads.
**Prevention:** Always enforce explicit maximum payload/buffer size limits (e.g., 10MB) in data handlers to prevent unbounded buffer memory exhaustion attacks in zero-dependency WebSocket servers.
