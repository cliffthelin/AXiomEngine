# Active ARCHON-GUIDES Checklist: server.md

- [ ] G-ARCHON-GUIDES-SERVER-001: Important: The server runs from the archon repo root — not the target repo. The `.env` file should already exist there (created in Step 4 of the setup wizard). (Section: Server Setup Guide)
- [ ] G-ARCHON-GUIDES-SERVER-002: SQLite (default): Autocreates at `~/.archon/archon.db`. No setup needed. (Section: 4. Database)
- [ ] G-ARCHON-GUIDES-SERVER-003: PostgreSQL (optional): Set `DATABASE_URL` in `.env` and run migrations: (Section: 4. Database)
- [ ] G-ARCHON-GUIDES-SERVER-004: tmux/screen: (Section: 5. Running in Background)
- [ ] G-ARCHON-GUIDES-SERVER-005: Docker (production): (Section: Ctrl+B, D to detach)
- [ ] G-ARCHON-GUIDES-SERVER-006: systemd (Linux): (Section: Ctrl+B, D to detach)
- [ ] G-ARCHON-GUIDES-SERVER-007: Only use one instance at a time per set of platform tokens — running multiple instances causes token conflicts. (Section: Important Notes)
- [ ] G-ARCHON-GUIDES-SERVER-008: The server must be running for Telegram, Slack, Discord, and GitHub platforms to work. (Section: Important Notes)
- [ ] G-ARCHON-GUIDES-SERVER-009: CLI workflows work independently and do not require the server. (Section: Important Notes)
- [ ] G-ARCHON-GUIDES-SERVER-010: Configuration: `~/.archon/config.yaml` is autocreated on first run with sensible defaults. Environment variables in `.env` override matching config values (e.g., `TELEGRAM_STREAMING_MODE` overrides `streaming.telegram`). (Section: Important Notes)
