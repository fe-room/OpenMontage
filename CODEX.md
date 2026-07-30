# OpenMontage - Codex Agent Instructions

> **Start here:** See [`AGENT_GUIDE.md`](AGENT_GUIDE.md) — the complete operating guide and agent contract.
> **Project context:** See [`PROJECT_CONTEXT.md`](PROJECT_CONTEXT.md) for architecture, key files, and conventions.

## Codex Host Capability

For generated still images, default to the `imagegen` skill and built-in
`image_gen` tool.
It is available outside the OpenMontage Python registry, so follow the Codex
override in `AGENT_GUIDE.md` even when `image_selector` reports no configured
provider. Keep all outputs and provenance inside the normal project workspace
and pipeline artifacts.
