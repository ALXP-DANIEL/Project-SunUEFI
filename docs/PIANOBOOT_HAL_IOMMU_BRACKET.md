# HALIOMMU startup boundary: next display diagnostic

**Status: INCOMPLETE_NOT_RELEASE, offline candidate; physical test pending.**

The operator's recorded visual-stage sequence reached purple marker
`13` (white tiles 0/2/3 from the left), then changed to a white panel
without a visibly drawn orange marker for driver13. Exactly 13 native
`StartImage` attempts are indexed in this source; entry13 is HALIOMMU.
The prior purple marker occurred **before** the SMMU/CPU mapping/clock
observers, not immediately at the vendor driver call.

This candidate keeps the earlier pixel markers and inserts two additional
*only* for HALIOMMU. The hook in NativeProbe emits a marker after
`mNativeObserver(name,TRUE)` returns but before
`gBS->StartImage(Handle,NULL,NULL)`; a second hook emits after StartImage
returns but before `mNativeObserver(name,FALSE)`. Both markers render via
the inherited GOP VideoFill path and pause for 1.5 s. No direct physical
framebuffer access, vendor HAL patches, bypassed driver, or clock/power/
SMMU register write is introduced by these markers.

| Color | Marker | Physical interpretation if visible |
|---|---|---|
| Purple with tile pattern 13 | Before pre-driver observers | Existing known visible boundary |
| **Yellow** with tile pattern 13 | After pre-driver observers / immediately before StartImage | Observer code returned without visibly blanking scanout |
| **Lime green** with tile pattern 13 | Immediately after StartImage returned, before post-driver observers | HALIOMMU StartImage returned with scanout still visibly updating |
| Orange with tile pattern 13 | After post-driver observers | Post-observer returned and scanout still visible |

If purple is last, isolate the pre-driver observers; if yellow is last,
isolate HALIOMMU StartImage and its SMMU/display mappings; if lime is last,
isolate post-driver observation. If all four are seen, move focus to the
subsequent foundation/UFS handoff. Distinctive color transitions, **not**
bootloader `OKAY` or GOP `EFI_SUCCESS`, are physical evidence.

The preceding build was temporary-booted twice and did not enumerate over USB.
The current candidate has **not** yet been booted and Android recovery
after the repeated physical run is unconfirmed. Avoid another physical
attempt until recovery and device state are known. Do not flash this image.
