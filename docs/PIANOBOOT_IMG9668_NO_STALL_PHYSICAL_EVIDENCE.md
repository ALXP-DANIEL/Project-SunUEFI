# IMG_9668 physical observation — ClockDxe no-return-Stall candidate

**Result:** camera-confirmed white display after native `ClockDxe` returns.
**Physical recovery after this run:** not confirmed. **Do not auto-retry.**

## Reproducible identities

- Original operator video: `IMG_9668.MOV`, duration ~12.573 s, 3840x2160,
  SHA-256 `ceced033f6d41f820967ea43293252b9b567e29c2c928af13548ede840ec7097`.
- Candidate branch `experiment/pianoboot-clockdxe-no-return-stall`, source
  commit `cfa55322f52941bbd1855b6aac5e1b8e52bd448b`, GitHub CI run
  `38116515133`, successful.
- Exact boot image `PianoUEFI-product.img` SHA-256
  `8c6380e2aeb354cda4cf6718e864713d1d154146656ca79c2d47763d8a13af66`,
  2,039,808 bytes, Android boot header v3, `INCOMPLETE_NOT_RELEASE`.
- The host verified Android `sys.boot_completed=1`, slot A, battery 100%,
  original bootloader Fastboot `product=piano`, `current-slot=a`,
  `unlocked=yes`, `is-userspace=no`; one temporary `fastboot boot` accepted
  the image. No `fastboot flash`, erase, automatic retry or recovery executed.
  ADB/Fastboot did not re-enumerate in the bounded ~30-second observation.

## Camera observations (times relative to the 12.6-second clip)

| Approx. time | Recorded image | Supported conclusion |
| --- | --- | --- |
| 3.75 s | Purple with tile bits 1 and 3 set (ordinal 10) | An earlier native start, **not** ClockDxe ordinal 13 |
| 5.75 s | Cyan/mint-looking display with ordinal-10 tiles | Prior ordinal's display; **not** evidence of post-ClockDxe observer completion |
| 9.75 s | Purple `CLOCKDXE` with white tile bits 0, 2, 3 (ordinal 13) | Camera confirms actual name and ordinal |
| 10.50 s | Bright lime `CLOCKDXE`, ordinal 13 | `StartImage` returned as far as the matching visible return witness |
| 11.60 s | Uniform white panel | Physical scanout is no longer showing diagnostic pixels |

No orange or mint **for ordinal 13 after its lime return marker** is visible
in this recording. The preceding cyan/mint-looking segment has ordinal-10
tiles, so it cannot be used to claim that ClockDxe's post-observers completed.

This candidate sets the special ordinal13 `ClockDxe` return-side `PauseUs=0`;
the firmware does **not call** `gBS->Stall` on that path. The subsequent
post-native observer's **orange entry** is configured to hold for 1.5 seconds,
but orange is not physically shown. The screen still retains the lime image
for ~1.5 seconds before it becomes white. Camera duration alone cannot show
that a CPU stall ran for that long: the framebuffer/GOP calls and panel
scanout can diverge. Neither `EFI_SUCCESS` from GOP nor a stale last image
proves the firmware is executing or halted after the return witness.

## Historical evidence and next offline investigation

Prior **Test101** (`docs/piano-product-test101.md`) measured GCC display AHB
at `0x127004` changing `0x88000003` to `0x88000002` between pre/post
`ClockDxe`. That test's complete log and working USB Fastboot show its CPU
continued after the clock transition, **in that distinct product build**.
The measured bit loss fits panel scanout failure, but does not establish a
cause for this SunUEFI-hosted image. Test103 independently re-acquired a real
AHB ref in a different product profile; its notes explicitly leave physical
panel success unproven. Test105 also warns against confusing cached Clock
resource votes with applied NPA rail state.

1. Compare the exact pinned `ClockDxe` PE/DEPEX/resource identity and its
   clock-ref handoff against Test101/103 evidence and the current product.
2. Find an independently validated, non-screen progress receiver before
   authorizing another physical startup candidate; host-visible USB absence
   and GOP-reported paint success alone are insufficient to localize a halt.
3. Keep diagnostic probing read-only and bounded. Do not force display
   clocks, rewrite clock registers, disable `ClockDxe`, assume a power-key
   reset duration, or flash persistent partitions from this evidence.

**Conclusion:** the no-Stall contrast reproduces lime-to-white, and further
delay-only boot experiments offer little new discrimination. Recovery into
ordinary Android is a prerequisite to any future separate physical test.
