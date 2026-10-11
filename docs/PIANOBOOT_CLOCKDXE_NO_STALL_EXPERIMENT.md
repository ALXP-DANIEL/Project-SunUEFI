# ClockDxe ordinal13 post-return no-Stall visual diagnostic

**Status:** offline-only follow-up; `INCOMPLETE_NOT_RELEASE`. This candidate
has not been physically tested. Do not flash or automatically boot it.

## New camera evidence: IMG_9666.MOV

- Original recording SHA-256:
  `71e9dbf4e848b00993fbf9c6b84580958d495144e516b0d432acd246c638e9eb`.
- Source image: SunUEFI hosted timing experiment at commit `379fd96`,
  SHA-256 `58afcfc5c020f2bbcb58574b252555627dfffe9bb529ec2eb0fed7a600929ea0`.
- The camera shows **purple CLOCKDXE at about 18.3 s**, **lime CLOCKDXE
  starting at about 18.8 s**, and **white at about 20.3 s**. Neither orange
  nor mint for ordinal13 is visible after lime.
- The previous build explicitly requests just 250,000 microseconds of
  `gBS->Stall` immediately after the lime paint, but the last visible lime
  image persists for about 1.5 s before scanout becomes white. Visible
  duration does **not** establish how long firmware spent inside `Stall`:
  the GPU/display may have stopped updating independently, a timer may have
  changed, or firmware may have stopped progressing.

## Isolated contrast

Only when `mVisualNativeIndex == 13`, the driver is **exactly `ClockDxe`**,
and the launch observer is on its return side:

1. Paint the **lime** `StartImage`-returned witness without a following
   `gBS->Stall` call (`PauseUs = 0`). The GOP paint and name remain unchanged.
2. Immediately enter the existing post-native observer callback, which first
   paints **orange** and then calls its existing 1.5 s stall **before** any
   of the three display observer operations.
3. Paint **mint** only if all post-native observers complete. Keep the
   native driver, dependency/order gates, observers and all other pauses
   identical to the prior image.

The change is deliberately narrow: no PLL/MMIO writes, modeset, DDR mapping,
slot switching, flash, or reset code. `Stall(0)` is not substituted for
`Stall(250000)`; `VisualProbe` skips calling `Stall` entirely when `PauseUs=0`.

## Interpretation limits

- **Orange after lime:** execution reached and painted the post-native callback;
  it would support a problem at or after the previous return-side delay, but
  it **does not** prove the actual post-native observation functions ran,
  because their orange hold precedes them.
- **Mint after orange:** all post-native observers returned, though a later
  or asynchronous scanout loss may still follow.
- **Lime then white again, no orange:** the camera alone cannot distinguish
  a GOP/scanout failure from stalled or stopped firmware, even after removing
  the explicit return-side stall. Do **not** claim `ClockDxe` crashed.
- **White without useful markers:** no inference about the CPU is possible.

The last temporary boot did not re-enumerate over ADB or Fastboot during
the bounded observation window. Require a **new Android recovery observation**,
exact candidate identity, valid battery and original Fastboot product/slot/
unlock/userspace checks, plus one-shot user authorization, before any physical
test. Conditional ABL boot-metadata effects remain unresolved.
