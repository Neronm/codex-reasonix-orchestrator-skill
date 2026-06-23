# Plugin Packaging

## Goal

Package the repo so the workflow can later be distributed as a Codex plugin, while keeping the skill directly usable from `skills/reasonix-orchestrator/`.

## Minimum Plugin Manifest

Place the manifest at:

```text
.codex-plugin/plugin.json
```

Recommended minimum fields:

* `name`
* `version`
* `description`
* `author.name`
* `license`
* `skills`
* `interface.displayName`
* `interface.shortDescription`
* `interface.longDescription`
* `interface.developerName`
* `interface.category`
* `interface.capabilities`
* `interface.defaultPrompt`

## Plugin Boundary

This plugin should point at:

```json
{
  "skills": "./skills/"
}
```

Do not guess URLs or marketplace metadata if the repo is not published yet. Use docs `TODO` notes instead.

## Installation Notes

Two install paths usually exist:

* skill-only install by copying `skills/reasonix-orchestrator/`
* plugin-form install using `.codex-plugin/plugin.json`

If the exact GitHub or marketplace install command for the target Codex build is unknown, say so explicitly and mark `TODO` in user-facing docs instead of inventing one.
