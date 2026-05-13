# Active ARCHON-GUIDES Checklist: cli.md

- [ ] G-ARCHON-GUIDES-CLI-001: No `.env` required: CLIonly usage doesn't need any environment variables. If no API keys are in the environment, the CLI autodefaults to global Claude auth from `claude /login`. (Section: Notes)
- [ ] G-ARCHON-GUIDES-CLI-002: Database: SQLite autocreates at `~/.archon/archon.db` — no setup needed for CLIonly use. (Section: Notes)
- [ ] G-ARCHON-GUIDES-CLI-003: Config: `~/.archon/config.yaml` is autocreated on first run with sensible defaults. Perrepo config can be added at `<repo>/.archon/config.yaml` to override the AI assistant or configure command folders. Neither file needs manual creation for basic usage. (Section: Notes)
