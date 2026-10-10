# PianoBoot on SunUEFI — experimental APPv1 integration

This branch is based on the **actual physically booted** SunUEFI source revision
`6a8763d010adb00b18911d6d12e6dd02869f98b9`. It retains SunUEFI's
independent SEC, DXE, BootShim, GOP, USB service, hardware providers and product
packaging rather than trying to boot PianoBoot's unrelated native FD.

It builds and seals the upstream SimpleInit sources as normal but selects
`uefi/applications/PianoBoot.efi` for the product's APPv1 payload. The
experimental app is the user's real 24,576-byte ARM64 EFI application from
PIANO BOOT commit `c34acac`, SHA-256
`c95e79c1b235ae1b8b91d29db66ef4e873cf6f477a19f8434ce59e2794460d9d`.

The `product_application.py` helper checks the exact embedded EFI byte digest
and architecture/subsystem, generates the 64-byte APPv1 header, and verifies
payload bytes and digest. ProductCore's generated digest header is recompiled
with this identity; package_product.py rechecks the exact payload against the
selected app and the sealed product manifest. No historical SimpleInit build
receipt is falsified.

The runtime application's cooperative SunUEFI pump integration is **not**
proved. Unlike SimpleInit, this PianoBoot application was not linked with its
GUI-loop pump. The physical screen's white transition and persistent USB
commands may remain broken. We have not proved that the menu renders, that
firmware reset works under this application, or that the modified product
preserves every function of upstream SunUEFI.

For a build on GitHub Actions, select the branch containing this change,
`Build products` workflow, `uefi` target. The build will emit
`PianoUEFI-product.img` inside the `piano-uefi-...` artifact. Build success
is not a substitute for operator review of the exact binary and reset plan.

**This branch must not automatically flash, boot or install a device image.**
