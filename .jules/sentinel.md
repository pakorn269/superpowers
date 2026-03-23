## 2025-02-15 - [Cross-Site WebSocket Hijacking in Brainstorm Server]
**Vulnerability:** The local WebSocket server in `skills/brainstorming/scripts/server.js` allowed any website to connect and send mock choice events to Claude without an Origin check.
**Learning:** Local dev tools that bind WebSocket servers must enforce strict `Origin` validation, as browsers automatically forward credentials and can silently connect to localhost services.
**Prevention:** Always validate `req.headers['origin']` against allowed hosts (`localhost`, `127.0.0.1`, or configured `HOST`) in the `upgrade` handshake of custom WebSocket servers.

## 2025-02-15 - [Unbounded Buffer Exhaustion in Brainstorm WebSocket Server]
**Vulnerability:** The custom WebSocket parser in `skills/brainstorming/scripts/server.js` continuously appended incoming chunks to a buffer without any size limit, allowing a malicious client to exhaust server memory (Denial of Service) by sending partial frames that never complete.
**Learning:** Stream-based protocol parsers (like custom WebSockets) must explicitly bound resource allocation, but limits must be applied carefully (after processing valid frames) to avoid falsely triggering on legitimate multi-frame chunks.
**Prevention:** Always enforce explicit maximum buffer size limits (e.g., 10MB) in data handlers, placed after the inner processing loop that extracts valid frames.
