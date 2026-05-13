# Active ARCHON-RULES Checklist: transitions.md

- [ ] G-ARCHON-RULES-TRANSITIONS-001: Transitions (`<TransitionSeries.Transition>`) — crossfade, slide, wipe, etc. between two scenes. Shortens the timeline because both scenes play simultaneously during the transition. (Section: TransitionSeries)
- [ ] G-ARCHON-RULES-TRANSITIONS-002: Overlays (`<TransitionSeries.Overlay>`) — render an effect (e.g. a light leak) on top of the cut point without shortening the timeline. (Section: TransitionSeries)
- [ ] G-ARCHON-RULES-TRANSITIONS-003: `presentation` — the visual effect (e.g. `fade()`, `slide()`, `wipe()`). (Section: Transition props)
- [ ] G-ARCHON-RULES-TRANSITIONS-004: `timing` — controls speed and easing (e.g. `linearTiming()`, `springTiming()`). (Section: Transition props)
- [ ] G-ARCHON-RULES-TRANSITIONS-005: `durationInFrames` — how long the overlay is visible (positive integer). (Section: Overlay props)
- [ ] G-ARCHON-RULES-TRANSITIONS-006: `offset?` — shifts the overlay relative to the cut point center. Positive = later, negative = earlier. Default: `0`. (Section: Overlay props)
- [ ] G-ARCHON-RULES-TRANSITIONS-007: Without transitions: `60 + 60 = 120` frames (Section: Duration calculation)
- [ ] G-ARCHON-RULES-TRANSITIONS-008: With transition: `60 + 60  15 = 105` frames (Section: Duration calculation)
