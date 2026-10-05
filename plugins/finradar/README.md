# FinRadar connected plugin

One shared skill and one hosted connection support Codex and Claude. The skill
uses current tool definitions from the connected service instead of a copied API
catalogue. A normal query does not run an updater or fetch documentation first.

## Install once and receive updates

Use the published GitHub marketplace at https://github.com/finradar-ai/plugins.
Both clients install the same released skill and hosted FinRadar connection.
A FinRadar account is required; complete the client's normal connection sign-in
when prompted. This does not choose or change your OpenAI or Anthropic account.

### Codex

Run these commands once from a terminal with Codex installed:

~~~sh
codex plugin marketplace add finradar-ai/plugins --ref main
codex plugin add finradar@finradar
~~~

The FinRadar source must remain a Git marketplace tracking main. Codex 0.158
includes a native background startup refresh for configured Git marketplaces
and their installed plugin copies. Start a new client session to load an update;
a successful package publication does not prove a running session has loaded it.
For an immediate refresh of this marketplace only:

~~~sh
codex plugin marketplace upgrade finradar
~~~

Check the installed entry with:

~~~sh
codex plugin list --marketplace finradar --json
~~~

Command reference: https://learn.chatgpt.com/docs/developer-commands#codex-plugin
Native startup behavior for the inspected version:
https://github.com/openai/codex/blob/rust-v0.158.0/codex-rs/core-plugins/src/manager.rs

### Claude Code

Run these commands once from a terminal with Claude Code installed:

~~~sh
claude plugin marketplace add finradar-ai/plugins
claude plugin install finradar@finradar
~~~

Then open /plugin in Claude Code, select Marketplaces, select finradar, and
choose Enable auto-update. Third-party marketplaces have automatic updates off
by default. This is a one-time customer setting, not a setting the package can
silently change. Administrators can use the documented autoUpdate setting on
this same marketplace instead of introducing a separate updater.

With automatic updates enabled, Claude Code checks in the background after the
first message in an interactive session, with a random delay of up to ten
minutes. Downloaded versions load on the next launch, or after /reload-plugins.
Client update-disabling settings and organizational restrictions still apply.
An immediate update of FinRadar only is also available:

~~~sh
claude plugin update finradar@finradar
~~~

Check the installed entry with:

~~~sh
claude plugin list --json
~~~

Update behavior and settings:
https://code.claude.com/docs/en/plugins/loading#when-auto-update-runs

### Existing installations and release verification

An installation already tracking this GitHub marketplace needs no reinstall
for each release. A local development folder or manually downloaded archive
needs a one-time migration to the published marketplace. Verify the new source,
installed version and connection before retiring the old FinRadar entry. Keep
other plugins and account settings unchanged. Do not keep two active FinRadar
copies or maintain the old development folder as a second release source.

The release command automatically prepares both formats and publishes changed
package content with an increased version after its checks pass. API-only or
data-only changes can leave this small connection package unchanged: financial
data and tool definitions are supplied by the hosted service. Provider refresh,
permissions and review rules govern when changed tools become visible.

The existing release checker runs the offline package and publication tests.
Public repository readback proves the released files; installed-version readback
proves a client received them. Neither alone proves a financial query succeeds.
This GitHub installation route serves local Codex and Claude Code clients.
Public directory approval and website-account installation are separate steps.

## Contents and build

- `skills/finradar-api/SKILL.md`: stable connected-research instructions.
- `.mcp.json`: the existing HTTPS FinRadar connection, without credentials.
- `.codex-plugin/plugin.json`: canonical package metadata and Codex presentation.
- `.claude-plugin/plugin.json`: generated Claude compatibility metadata.
- `.claude-plugin/marketplace.json`: generated Claude catalog pointing at this
  same package, with its category and display metadata from the canonical source.
- `scripts/package_plugin.py`: generates both Claude files, checks consistency,
  and creates a deterministic `.plugin` ZIP from an explicit file allowlist.
- `legal/privacy-policy/index.html`: canonical script-free public privacy policy.

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

Before the publisher updates the generated GitHub distribution, it requires the
public `https://mcp.finradar.ai/privacy-policy/` response to be byte-identical to
the committed package file. The dedicated MCP Nginx edge serves that committed
file read-only. A missing page, redirect, wrong content type or byte mismatch
stops the release before the public plugin repository changes.

The same publisher requires OpenAI's public domain-verification address to
return the one-line value stored in the exact approved server commit as plain
text. A missing route, redirect, HTML response, extra byte or different value
stops publication before the generated GitHub distribution changes.

The publisher never submits provider listings or changes installed clients.
Initial installation, provider review and host update permissions still apply.

Local development folders are development snapshots. Customers should install
from the public GitHub marketplace above; do not maintain personal folders as a
second release source. Migrate existing local installations through the client's
installation flow, verify the released copy, then retire the old catalogue entry.

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
https://code.claude.com/docs/en/discover-plugins#keep-plugins-updated

This package does not create a public directory listing, publish itself,
force a client refresh, or prove fresh-client authorization or improved latency.
The separately published standalone API skill remains unchanged and continues to
be generated by FinRadar's existing documentation build.
