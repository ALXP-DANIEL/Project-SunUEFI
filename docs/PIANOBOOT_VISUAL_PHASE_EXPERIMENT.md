# Physical display regression stage-marker experiment (offline candidate)

Test24 (confirmed working again as Test97) displayed an interactive SimpleInit.
Test25 first recorded a blank/grey screen after introducing native foundation
and touch dependencies. Current hosted PIANO BOOT and GCC-AHB builds show
TianoCore and then white on the same device. Test95 showed software framebuffer
pixels despite a white panel. These observations do not prove ClockDxe alone
is responsible.

This branch is based on the USB-cooperative PianoBoot integration
`afa01a3`, NOT the GCC-AHB-clock experiment `303c134`. Product hardware
providers and call order are unchanged. No native driver is disabled; no clock,
power, MMIO or display mode registers are written by the instrumentation.

An experimental compile flag adds GOP VideoFill-only markers to the existing
boot-log canvas at precise product boundaries. Each marker fills the screen with
one distinctive color plus six large black/white tiles. The white tiles
represent the binary native StartImage ordinal, LSB at the LEFT. A camera can
decode the last visible stage even when USB stalls. Actual native order is
recorded by firmware logs, not assumed from the image list, as DEPEX may change
which drivers start.

| Phase code | Full-screen color | Where | Pause |
|---|---|---|---|
| 0 | Blue | After payload validation, before foundation or observers | 3.5 s |
| 1 | Purple | Immediately before a native StartImage | 0.5 s |
| 2 | Orange | Immediately after a native StartImage returns | 0.5 s |
| 3 | Green | After entire native foundation finishes | 3.5 s |
| 4 | Cyan | After UFS probing | 1 s |
| 5 | Red | After USB service startup attempt | 0.5 s |
| 6 | Navy | Before product boot policy/menu | 1 s |

Only a screen seen by the physical observer is a display result. A valid GOP
Blt status or a screenshot of RAM pixels is NOT scanout acceptance. If blue is
physically visible then the screen later becomes blank, compare the last
visible color+ordinal to the selected native StartImage sequence. If blue is
never visible, narrow the earlier payload/BDS/boot-log boundary instead.
None of these phase names proves which display clock/power/scanout state changed.

The instrument works only while inherited GOP is available and the
original boot-log initialized. A failed Blt is recorded and no longer
attempted in that session. It never directly accesses framebuffer physical
memory or silently treats a warning as success. Stage delays do temporarily
block the foreground, including any cooperative USB work, and are solely for
physical observation; this build is NOT_RELEASE. Do NOT flash, install, or use
it as an OS boot candidate. On-device testing is a separate, one-shot temporary
`fastboot boot` experiment only after independent binary verification.

## First physical run: transport result, panel observation pending

- Source/build commit: 18fbf90df93d456dd093f9848e0157fed48510c2
- GitHub build: 38063685628, successful
- Boot image SHA-256: 034d007815a08ffb5bd3b68ac079a8495196f714615deaa799a534b6732dc40d
- Pinned EFI app SHA-256: b87410a92aeea6a6c07d7edefe6b51e1c3cae4bee8a7f4951eec3467848688a9
- The original BootShim and DTB were independently verified byte-identical
  to the prior successfully booted upstream control.
- Tablet before test: Lineage Android boot-complete 1, battery 100 percent,
  original Xiaomi fastboot product piano, unlocked yes, slot a, userspace no.
- One temporary fastboot boot succeeded: 1992 KiB sent, 0.047 s transfer,
  boot accepted in 0.222 s, no flash command.
- Neither SunUEFI Fastboot nor Android ADB enumerated during two bounded
  approximately 30-second observation windows after that boot.
- Physical panel colors/last ordinal: NOT REPORTED YET. Do not infer the
  last native driver, a blank panel, or which C function executed from the
  absence of USB alone.
- Android recovery after this precise run: NOT CONFIRMED YET. No additional
  boot attempt or automatic recovery command was sent.

Important interpretation: native startup delays and the large new GOP fills
are *interventions* in this run; the absence of USB within roughly a minute
does not independently identify the white-screen root cause. Await the
operator's visual marker record and Android recovery, then narrow the next
candidate. This binary is an instrument, not a fix.
