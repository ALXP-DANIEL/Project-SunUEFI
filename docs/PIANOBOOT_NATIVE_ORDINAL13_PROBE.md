# Camera-confirmed diagnostic correction: actual ordinal 13

**STATUS: INCOMPLETE_NOT_RELEASE. No additional physical boot performed.**

The second diagnostic video `IMG_9664.MOV` has SHA-256
`a7c0cca7ae98cd4cd8e6b8d3515ff5e521e0b290e3b9260b35a9b1a1dcfe9361`
and duration approximately 25.13 seconds. Frame timing is approximate.

The video establishes:

- At ~20.0 s the **lime-green** HALIOMMU *after-StartImage* marker
  shows ordinal **10**: white tiles at positions 1 and 3, LSB left
  (2 + 8 = 10). **HALIOMMU StartImage returned** and the panel still scanned
  out subsequently written frames. Therefore earlier documentation equating
  the 13th launch with HALIOMMU was WRONG.
- At ~20.4 s an orange after-StartImage marker for ordinal10 is visible,
  meaning the post-driver observer was **entered**, not necessarily completed.
- At ~20.8-21.4 s purple/orange frames show ordinal11
  (white positions 0,1,3; 1+2+8=11).
- At ~21.8-22.4 s purple/orange frames show ordinal12
  (white positions 2,3; 4+8=12).
- At ~22.8-23.2 s the final visible **purple** marker shows ordinal13
  (white positions 0,2,3; 1+4+8=13).
- At ~23.4 s onward the panel is white. No post-observer orange marker or
  exact entry yellow marker for ordinal13 is visible in the recorded interval.

**Causal scope:** NativeProbe executes ready DXE drivers in repeated
dependency passes, so `mNativeImages[12]` does **not** mean the 13th
actual native driver. Native image table location alone is insufficient
to identify ordinal13; no device UART/USB runtime driver-name log was
available from this test. Further, the purple marker is drawn *before*
three read-only/bounded pre-driver observations. Thus the white transition
is between the purple ordinal13 paint and a visible after-stage marker,
not proof the final driver's StartImage was entered or caused the change.

## Experimental ordinal-13 witness

Based on the previous HALIOMMU-bracket build `c3dbd61`, this separate
branch preserves every native DXE and retains the known-useful HALIOMMU
yellow/lime witnesses, then adds:

- A **white-on-color driver name strip** using the inherited GOP VideoFill
  and the already-host-tested 5x7 font. It is painted only for ordinal13,
  naming the actual runtime driver instead of assuming table order.
- **Yellow ordinal13:** Pre-driver observers returned and actual
  `gBS->StartImage` is about to be invoked.
- **Lime ordinal13:** Actual StartImage returned.
- **Orange ordinal13:** Post-observer function was entered.
- **Mint/teal ordinal13:** All three post-driver observers returned.

No native driver bypass, clock/power/MMIO write, GOP SetMode, direct
framebuffer access, boot-partition write or persistent flashing is
introduced. GOP color/label evidence is not a physical display guarantee.
If the name strip is not legible in a video, an unmodified runtime log
or independent test will still be required to identify the actual driver.
The colors and inserted delays may alter the timing of the hardware,
so results are diagnostic rather than proof of physical root cause.

The last physical test had no USB enumeration after approximately a
minute, and Android recovery has not yet been confirmed in this
conversation since that test. Do not automatically boot this candidate
until recovery is established; use a single RAM-only `fastboot boot`
for any future explicitly authorized experiment, **never flash**.
