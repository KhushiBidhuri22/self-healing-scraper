# Metrics

## Test Suite

25 tests passed.

## Chaos Recovery

Total mutations: 8
Recovered: 6
Failed: 2
Recovery rate: 75%

## Healing

Promotion threshold: 95%
Maximum healing attempts: 3

## Token Optimization

The healing system does not send the full page to an LLM
on the normal request path.

Candidate generation and scoring are deterministic.

Successful selector repairs are cached and reused.

## Latency

API latency should be measured separately for:
- cold request
- warm request
- cached request

## Known Failure Cases

### lazy_load
The required product fields are removed from the DOM.
The system correctly refuses to invent missing data.

### remove_price
The price element is removed completely.
The system detects the missing field but does not fabricate a price.

These failures are intentional demonstrations of safe
failure rather than false recovery.