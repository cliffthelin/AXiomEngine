# Active ARCHON-RULES Checklist: audio-visualization.md

- [ ] G-ARCHON-RULES-AUDIO-VISUALIZATION-001: `numberOfSamples` must be power of 2 (32, 64, 128, 256, 512, 1024) (Section: Spectrum Bar Visualization)
- [ ] G-ARCHON-RULES-AUDIO-VISUALIZATION-002: Values range 01; left of array = bass, right = highs (Section: Spectrum Bar Visualization)
- [ ] G-ARCHON-RULES-AUDIO-VISUALIZATION-003: Use `optimizeFor: "speed"` for Lambda or high sample counts (Section: Spectrum Bar Visualization)
- [ ] G-ARCHON-RULES-AUDIO-VISUALIZATION-004: Important: When passing `audioData` to child components, also pass the `frame` from the parent. Do not call `useCurrentFrame()` in each child  this causes discontinuous visualization when children are inside `<Sequence>` with offsets. (Section: Spectrum Bar Visualization)
