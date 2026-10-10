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
