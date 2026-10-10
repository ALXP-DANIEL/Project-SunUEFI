# PianoBoot on SunUEFI — experimental APPv1 integration

This branch is based on the **actual physically booted** SunUEFI source revision
`6a8763d010adb00b18911d6d12e6dd02869f98b9`. It retains SunUEFI's
independent SEC, DXE, BootShim, GOP, USB service, hardware providers and product
packaging rather than trying to boot PianoBoot's unrelated native FD.

It builds and seals the upstream SimpleInit sources as normal but selects
`uefi/applications/PianoBoot.efi` for the product's APPv1 payload. The
experimental app is the user's real 28,672-byte ARM64 EFI application from
PIANO BOOT commit `69647c3`, SHA-256
`b87410a92aeea6a6c07d7edefe6b51e1c3cae4bee8a7f4951eec3467848688a9`.

The `product_application.py` helper checks the exact embedded EFI byte digest
and architecture/subsystem, generates the 64-byte APPv1 header, and verifies
payload bytes and digest. ProductCore's generated digest header is recompiled
with this identity; package_product.py rechecks the exact payload against the
selected app and the sealed product manifest. No historical SimpleInit build
receipt is falsified.

The application now probes SunUEFI's optional revision-1 runtime protocol
and cooperatively calls its service Pump while polling the input keyboard;
without that protocol it uses its existing UEFI event wait. This avoids the
previous unbounded wait that could starve the USB service. The modified
application was rebuilt and passed the ArmVirt/QEMU menu/keyboard/diagnostics
regression (which does **not** exercise the real SunUEFI provider). Actual
USB-service pumping, recovery, and the physical white-screen issue are still
**unvalidated on the tablet**. Do not treat a successful build as evidence
that the graphical menu will be visible.

For a build on GitHub Actions, select the branch containing this change,
`Build products` workflow, `uefi` target. The build will emit
`PianoUEFI-product.img` inside the `piano-uefi-...` artifact. Build success
is not a substitute for operator review of the exact binary and reset plan.

**This branch must not automatically flash, boot or install a device image.**
