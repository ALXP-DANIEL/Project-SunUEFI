# PIANO BOOT hosted GCC-AHB owner + camera probe contrast

**State:** offline experimental candidate, `INCOMPLETE_NOT_RELEASE`. It is
**not** an authorized physical boot, production repair or install image.

## Why this candidate exists

Video `IMG_9668.MOV` of commit `cfa5532` shows ordinal13 `ClockDxe`'s
lime `StartImage` return witness, then a white panel with **no observed
orange or mint for ordinal13**. The change that removed the return-side
stall did not restore physical scanout. Nothing in that video independently
proves CPU progress or the display clock's live enable state after lime.

Old **Test101** measured GCC display AHB register `0x127004` switching from
`0x88000003` to `0x88000002` inside a *different*, unmodified ClockDxe
candidate. Its finding cannot be directly copied to the current hosted
firmware. This build instead stages the audited, pinned **derived** ClockDxe
SHA-256 `3f459c822c8d8f87ca832b37709c3b56548319bfe60ff01ffd37ddc56d72d967`.
That patch skips the CESTA cleanup for **seven** camera/display resources
and defers display CESTA/PLL automatic initialization. Retention is not
display-only; typed shutdown of those seven native references is unproved.
The original Test101 enable-bit transition might therefore **not occur** in
this product. No currently recorded image/video includes the required live
register comparison for the derived ClockDxe.

## Minimal integration of existing native ownership code

Reuse original experimental commit `303c134` *alongside*, not instead of,
the current ordinal13 name/color markers:

- The regular native foundation and all observer callbacks still run. No
  driver is bypassed, including HALIOMMU and ClockDxe.
- After `PianoProbeFoundation()` finishes, and before UFS/USB/menu, acquire
  precisely one `gcc_disp_ahb_clk` reference through the already implemented
  `PianoProductDisplayStartAhbOnly()` path. It validates pinned native image,
  actual typed clock ID, two independent reference snapshots, enabled-state
  output, and bounded, protected GCC readback; no direct register write.
- Deliberately **do not** acquire the separate experimental non-GDSC child
  or MM/VCS rail owner. This is not full DPU/DSI/panel ownership.
- Wire the *actual* returned held-reference report into the existing product
  owner manager, whose cooperative stop must release exactly the acquired
  reference. Any retained, ambiguous or partially successful acquisition
  fails closed; only proven no-side-effect refusal may be represented absent.
- Keep the existing `PIANO_EXPERIMENT_DISPLAY_PHASE_PROBE` enabled so a
  later camera comparison has the same 13th-driver identification markers.
  Do not claim that the observer images prove hardware scanout readiness.
- Pin the derived ClockDxe SHA-256 in product preparation and mark the
  extra hardware-mutating owner flag and physical-test-unvalidated status
  explicitly in the build manifest.

**Important limitation:** The new clock acquisition happens **after** the
entire native foundation and its observers. If the white screen is caused by
an earlier fatal stop, this code will never execute. If GOP scanout dies
before this point, a later AHB reference may not automatically restore it.
The contrast checks an existing hardware ownership mechanism, **not** a
guaranteed fix. Source compilation and host simulations cannot prove the
physical display works or the AHB bit was previously disabled.

## Verification and physical gate

Host tests must cover the GCC-only case, clean release, non-leaking clean
refusal and retained partial failure; also the camera probe's untouched
native order, exact flags, and the actual product build. The 30-case native
coordinator tests do not execute tablet hardware.

Do not boot this image without a **separately reviewed** physical plan:
fresh Android recovery confirmed, known exact image SHA-256 and CI manifest,
original Fastboot `product=piano`, active slot, unlock and userspace gates,
and an independently trusted recovery method. The installed ABL may make
conditional persistent boot-metadata changes even for `fastboot boot`.
No `fastboot flash`, erase, slot change, direct clock-register patch,
or automatic retries are allowed by this experiment.
