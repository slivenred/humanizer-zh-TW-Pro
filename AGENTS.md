# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

This repository is a Markdown skill for Codex, Claude Code, OpenCode, and compatible agents. The runtime artifact is `SKILL.md`; there is no build step and no CLI.

## Key files

- `SKILL.md` is the product and the source of truth.
- `README.md` is the human-facing installation and usage guide.
- `LICENSE` must preserve upstream MIT notices.

## Maintenance contract

- Keep the pattern count at 33 unless deliberately adding, removing, or renumbering patterns.
- If pattern names, behavior, or numbering change in `SKILL.md`, update the README table in the same change.
- Keep the version in `SKILL.md` metadata and README version history in sync.
- Preserve the Taiwan Traditional Chinese focus. Do not turn this back into a literal translation of the English source.
- Preserve the SEO and fact-retention rules. Do not add guidance that encourages inventing facts, prices, rankings, citations, dates, or source claims.
- Preserve false-positive guidance. The skill should not flatten already-good writing just to remove isolated words.

## Editing style

- Edit the prompt like an editor, not like code.
- Use examples that sound natural to Taiwan readers.
- Avoid internal prompt language in examples of publishable output.
- Avoid broad formatting churn.
