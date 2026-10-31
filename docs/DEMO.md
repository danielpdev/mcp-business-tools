# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

The MCP server exposes inventory reads and order preparation. Capability scopes come from the server process, never from tool arguments. Stock is committed only through a separate operator approval surface.

## Failure case to discuss

Real stdio client/server initialization, tool discovery, forbidden capabilities, invalid quantities, expiry, action fingerprints and approval replay.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Stdio deployment trusts the machine operator. The separate local approval API is not a production authenticated operator console. Preparing an order does not reserve stock.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
