# Active ARCHON-RULES Checklist: maps.md

- [ ] G-ARCHON-RULES-MAPS-001: Animations must be driven by `useCurrentFrame()` and animations that Mapbox brings itself should be disabled. For example, the `fadeDuration` prop should be set to `0`, `interactive` should be set to `false`, etc. (Section: Adding a map)
- [ ] G-ARCHON-RULES-MAPS-002: Loading the map should be delayed using `useDelayRender()` and the map should be set to `null` until it is loaded. (Section: Adding a map)
- [ ] G-ARCHON-RULES-MAPS-003: The element containing the ref MUST have an explicit width and height and `position: "absolute"`. (Section: Adding a map)
- [ ] G-ARCHON-RULES-MAPS-004: Do not add a `_map.remove();` cleanup function. (Section: Adding a map)
- [ ] G-ARCHON-RULES-MAPS-005: The progress is clamped to a minimum value to avoid the line being empty, which can lead to turf errors (Section: Animating the camera)
- [ ] G-ARCHON-RULES-MAPS-006: See [Timing](./timing.md) for more options for timing. (Section: Animating the camera)
- [ ] G-ARCHON-RULES-MAPS-007: Consider the dimensions of the composition and make the lines thick enough and the label font size large enough to be legible for when the composition is scaled down. (Section: Animating the camera)
