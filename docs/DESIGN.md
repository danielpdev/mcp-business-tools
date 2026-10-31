# Design record

## Decision

The MCP server exposes inventory reads and order preparation. Capability scopes come from the server process, never from tool arguments. Stock is committed only through a separate operator approval surface.

## Failure model

Real stdio client/server initialization, tool discovery, forbidden capabilities, invalid quantities, expiry, action fingerprints and approval replay.

## Tradeoffs

Stdio deployment trusts the machine operator. The separate local approval API is not a production authenticated operator console. Preparing an order does not reserve stock.

## Next change to defend in review

Add per-user authentication and reservation expiry without letting the model grant itself scopes.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
