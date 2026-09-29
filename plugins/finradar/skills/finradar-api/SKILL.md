---
name: finradar-api
description: Retrieves financial data through the connected FinRadar service when users ask about SEC filings, institutional holdings, insider transactions, beneficial ownership, or company financial statements. Intended for connected data queries, not direct HTTP integration development.
---

# FinRadar connected research

Use the authenticated FinRadar connection supplied by the host. Tool names,
parameters, supported filters, response fields and available capabilities come
from the connection's current tool definitions, not from a bundled API catalogue.

## Retrieve the requested data

- If the needed tool is already available with a sufficient definition, call it
  directly. Otherwise use the host's tool discovery to find the specific
  FinRadar capability needed. Do not dump the entire catalogue for one lookup.
- Follow the selected tool's advertised argument names, types and allowed
  values. Do not reconstruct a call from remembered API paths or old examples.
- Preserve documented defaults for filters the user did not request. Do not
  carry a date range, filing-version selection or other filter into an unrelated
  query. Presentation wording alone does not select a historical filing version.
- A missing cell or empty filtered result describes that request. Report its
  returned status and reason; do not infer global unavailability, replace a
  reported metric with your own calculation, or change the user's requested filters.
- Resolve missing or ambiguous identifiers through the relevant FinRadar lookup.
  Reuse identifiers already established in the conversation; do not repeat a
  resolved lookup or substitute an example identifier for the requested entity.
- Request the user's filters, ordering, reporting period and result count where
  the current tool supports them. Do not fetch unrelated enrichment.
- When a selected tool says its first text block is ready to display, return
  that text unchanged in a plain-text code block as the answer. Do not summarize, reformat, relabel,
  reorder, recalculate or reconstruct it from the structured response. Use the
  structured response only when the user asks for further analysis.
- Answer once sufficient data returns. Preserve the result's reporting date,
  units and source, and distinguish reported holdings from real-time positions.

## When more detail is necessary

Use the selected tool's current definition first. If it lacks a detail needed
to answer correctly, consult the current topic reference through
https://api.finradar.ai/llms.txt and open only the relevant linked section.
Do not fetch documentation or check for updates before an ordinary lookup whose
tool definition is already sufficient. An HTTP documentation example does not
require a separate API key for a working FinRadar connection.

## Connection boundary

Use the host's existing connection authentication. Do not inspect credentials,
ask for an API key, or launch a separate API helper to repeat connected access.
If FinRadar is not connected or authorization has expired, identify that
condition and use the host's normal Connect/sign-in flow with the user's consent.
Do not invent data or claim a tool is available when the host has not exposed it.

These instructions contain no API version, tool-name table, parameter schema,
pricing schedule or local endpoint reference to update when the API changes.
The host controls when it refreshes the server's tool definitions and approvals.
