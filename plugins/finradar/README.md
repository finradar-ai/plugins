# FinRadar connected plugin

One shared skill and one hosted connection support Codex and Claude. The skill
uses current tool definitions from the connected service instead of a copied API
catalogue. A normal query does not run an updater or fetch documentation first.

## Contents and build

- `skills/finradar-api/SKILL.md`: stable connected-research instructions.
- `.mcp.json`: the existing HTTPS FinRadar connection, without credentials.
- `.codex-plugin/plugin.json`: canonical package metadata and Codex presentation.
- `.claude-plugin/plugin.json`: generated Claude compatibility metadata.
- `.claude-plugin/marketplace.json`: generated Claude catalog pointing at this
  same package, with its category and display metadata from the canonical source.
- `scripts/package_plugin.py`: generates both Claude files, checks consistency,
  and creates a deterministic `.plugin` ZIP from an explicit file allowlist.

Run the packaging script with `--output-dir` to generate a release. Its `--check`
mode verifies consistency without writing. It refuses copied reference files,
extra skill helpers and mismatched generated metadata. Both clients use exactly
the same skill and connection files; neither maintains a separate API catalogue.

## Automated release preparation

The package directory in FinRadar's application repository is the release source.
Both frontend build commands
(`npm run build` and `npm run build:client-only`) first run
`npm run build:connected-plugin`. That invokes this same packager with
`--build-output-dir .generated/ai-plugins`, then checks the generated metadata.
Invalid input stops the documentation build. Python's standard library is the
only packaging dependency; the frontend Dockerfile installs it in the temporary
build stage, not the final website image.

The archive is written beneath `.generated/ai-plugins/<sha256>/finradar.plugin`.
Identical builds reuse the identical archive; changed content gets a new directory
without deleting or replacing an earlier archive. The command prints its path,
size and digest. These are private preparation artifacts, excluded from Git and
the incoming Docker build context, and are not copied into website assets or the
final nginx image. The release command consumes this packager's archive and digest
only after deployment and live publication verification pass. Building alone
does not publish, install, register or refresh anything.
Content identity is not a provider version: skill or listing changes still need
an appropriately versioned, reviewed release through the provider's channel.

## Automated public delivery

The generated distribution repository is https://github.com/finradar-ai/plugins.
It is not a second editing source. The approved release command prepares the
committed package in temporary storage and publishes after its existing live
checks. Its documentation-only mode replaces only the documentation service;
its publication-only mode verifies an already-deployed release without replacing
any service. Both use the same publisher. Direct manual server commands are not
the automatic release path.

The publisher generates both root catalogs, the shared plugin directory and
`finradar.plugin` from the same archive. Unchanged content causes no upload or
version bump. Changed content automatically advances the numeric patch version
(or uses a higher canonical release version). A non-forced, single Git update
publishes the complete tree. An older source commit, unexpected repository files,
competing release, failed request or failed readback stops completion; there is
no automatic rollback, service restart or background retry. The existing GitHub
login supplies repository access without adding secrets to the package or server.

The publisher never submits provider listings or changes installed clients.
Initial installation, provider review and host update permissions still apply.

The former personal package on the development laptop remains an unchanged
development snapshot, not a second release source. Do not maintain it separately.
Retire its standalone development role when an approved catalog migration points
clients at this repository's released package; this integration does not change
existing personal catalogs or installed plugins.

The Claude catalog is included in the release and regenerated on every build.
Generating it does not register a marketplace with Claude, install the plugin,
start authorization, or publish a public listing. Do not edit either generated
Claude file manually; change the canonical metadata and rebuild.

A FinRadar account and authorization through the client's connection flow are
required. No environment variables or manually copied API keys are required by
this connected package. Normal FinRadar usage charges still apply.

## Update contract and limits

API changes do not require changing this package's instructions or copying new
reference files into it. The FinRadar server remains the source of tool
definitions and financial data. Client discovery, caching, consent and platform
review still govern when changed definitions become available.

OpenAI periodically scans published MCP tool definitions and checks changes.
Published skill-content changes still require a new reviewed plugin version:
https://developers.openai.com/plugins/deploy/submission

Claude controls plugin updates through its host and marketplace settings:
https://code.claude.com/docs/en/discover-plugins#configure-auto-updates

This package does not create a public directory listing, publish itself,
force a client refresh, or prove fresh-client authorization or improved latency.
The separately published standalone API skill remains unchanged and continues to
be generated by FinRadar's existing documentation build.
