### SOURCE:
> Local copy of the advisory catalog. Canonical source in `templates/migration/catalogs/migration_strategies.md`.

# Migration Strategies (local copy)

## Strategies

### Strangler Fig
- **When applicable**: system in production, cannot be stopped; need for incremental approach; possibility of routing (proxy / API gateway).
- **Cost**: medium. **Risk**: low. **Time**: long.
- **Preferred appetite**: conservative, balanced.

### Big Bang
- **When applicable**: small system; acceptable downtime; transformational appetite; few live integrations.
- **Cost**: low. **Risk**: high. **Time**: short.
- **Preferred appetite**: transformational (in small systems).

### Parallel Run
- **When applicable**: critical logic (financial / fiscal / regulatory); requires proof of equivalence over a long period.
- **Cost**: high. **Risk**: medium. **Time**: medium.
- **Preferred appetite**: balanced.

### Branch by Abstraction
- **When applicable**: internal migration (language or framework changes, domain remains the same); conservative appetite.
- **Cost**: low. **Risk**: low. **Time**: medium.
- **Preferred appetite**: conservative.

## Recommendation rules

- `conservative` appetite → Branch by Abstraction + Strangler Fig.
- `balanced` appetite → Strangler Fig + Parallel Run.
- `transformational` appetite → Big Bang in small systems; Strangler Fig with deep boundaries in larger ones.
- large paradigm shift + transformational appetite → recommend Parallel Run to validate parity.
- system with regulatory integrations → never recommend Big Bang.

## Pseudo-procedure

1. Filter applicable strategies based on the brief.
2. Score the remaining ones based on adherence to the appetite and paradigm gap.
3. Select 2 to 3 candidates.
4. Mark one as recommended with justification.
5. For each other, list cons as the reason for non-recommendation.