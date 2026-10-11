# Camera-identified ClockDxe ordinal13 and post-return timing experiment

**Status:** offline-only experimental follow-up; `INCOMPLETE_NOT_RELEASE`.
**No physical boot of this follow-up image is authorized or claimed.**

## New physical evidence: IMG_9665.MOV

- Original recording SHA-256:
  `a33dca9995273f9973824af5a2207b2183cade097b111269b1342265c83891ba`.
- The source image is the readable-label SunUEFI hosted product (commit `b5e666b`,
  SHA-256 `2313b044111f68cf183527c0a9e72658306e585b6986807111b9273c286009f3`).
  The user authorized ONE temporary `fastboot boot`; host confirmed its
  transport success. No partition flash/erase was performed.
- Video ~21.0s: **purple with CLOCKDXE label**, six white/black tiles LSB-first
  giving actual runtime ordinal **13** (white positions 0,2,3).
- Video ~21.5–23.0s: **lime-green with CLOCKDXE label**, ordinal13: compiled
  `PianoProbeImmediatelyAfterStartImage` was visibly painted, demonstrating
  that **ClockDxe's `StartImage` returned**. Camera samples cannot prove whether
  subsequent callbacks continued after visible scanout stopped.
- Video ~23.1s: uniformly white panel. **No ordinal13 orange entry or mint
  post-observer-completion marker was visibly observed.** The ordinal13 yellow
  before-`StartImage` marker was also not individually resolved in the video;
  do not infer it was absent from execution.
- The lime duration is approximately the diagnostic's **1.5 s `Stall`**,
  which places the white transition near the return from that delay or
  the following post-native observer. This is a timing correlation, **not
  proof** that any particular post-observer caused the display loss.
- The tablet did not re-enumerate as ADB or Fastboot during a short bounded
  post-boot observation. Current Android recovery **not yet confirmed**.

## Next controlled contrast — no hardware-register intervention

Keep every native DXE, dependency gate and pre/post observer active. Only when
the current, dynamically counted ordinal is 13 **and** the driver's real
`Name` is `ClockDxe`:

1. Show the existing **lime** after-`StartImage` witness for **0.25 s**
   instead of 1.5 s.
2. Show the existing **orange** post-native observer entry witness for
   **1.5 s** instead of 0.5 s.
3. Leave the existing **mint** post-observer-completed witness for 1.5 s.

All other probe durations, including HALIOMMU, are unchanged. The experiment
does not skip ClockDxe or observers; it does not force a panel mode, read/write
new MMIO addresses, modify IOMMU mappings, switch slots, or flash partitions.

### How a future camera recording should be interpreted

- **Orange becomes visible:** the post-native callback was entered with
  scanout still able to update. Any later white event may reflect a delayed
  ClockDxe side effect, one of the observer operations or another change.
- **Mint becomes visible:** all three post-native observers returned, so any
  subsequent loss occurred after their completion, or asynchronous to them.
- **No orange or mint:** cannot distinguish a failed Blt/scanout from code
  that stopped before that marker; review offline and do not label an observer
  as the cause without independent evidence.

Inserted dwell changes affect timing and could alter the behavior being
investigated. Prior observed evidence is retained as a control. Independent
native ABL→SEC firmware remains a separate unproven track.

**Physical test gate:** require a fresh Android recovery observation, battery,
original-Fastboot product/slot/unlocked/userspace checks and verified exact
new boot-image hash before asking for a *new*, explicitly approved one-shot
temporary test. Do not auto-retry or presume `fastboot boot` is free from
possible conditional boot-metadata side effects in the installed ABL.
