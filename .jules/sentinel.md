## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2026-03-17 - [Unbounded Buffer DoS in Custom Protocol Parser]
**Vulnerability:** The local WebSocket server implementation in `skills/brainstorming/scripts/server.js` appended all incoming chunks to a memory buffer without any maximum size limit.
**Learning:** Custom stream-based protocol parsers (like zero-dependency WebSocket or HTTP servers) are highly susceptible to memory exhaustion (OOM) Denial of Service attacks if they allow unbounded buffer accumulation during data reception.
**Prevention:** Always implement explicit maximum payload or buffer size limits (e.g., `MAX_WS_PAYLOAD = 10MB`) in `socket.on('data')` handlers before concatenating incoming byte chunks.
