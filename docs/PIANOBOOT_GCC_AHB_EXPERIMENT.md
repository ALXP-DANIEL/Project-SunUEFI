# Experimental PIANO BOOT GCC display-AHB owner

The previous two SunUEFI-hosted PianoBoot images accepted temporary fastboot
boot and enumerated SunUEFI-piano, but the operator observed TianoCore splash
followed by a white physical panel. The getvar product command returned;
a later screenshot request stalled. Current menu render acceptance is unknown.
Android recovered normally.

The earlier baseline test24 (replayed successfully as test97) displayed
SimpleInit on the same tablet. Product tests95/103 demonstrated that graphical
menu pixels can be present in the UEFI framebuffer while the physical panel
is white. Test101 identified native ClockDxe clearing GCC display-AHB
enable bit0 at register 0x127004; test103 used a genuine pinned native
clock protocol to take a typed reference, restoring its readback from
0x88000002 to 0x88000003, and retired exactly one owned reference while
recovering Android. The physical panel outcome for test103 was NOT established.

In ProductCore, after native foundation initializes and before UFS/USB/menu,
the experimental branch calls PianoProductDisplayStartAhbOnly() and retrieves
a typed startup report. This variant:

- Acquires one verified GCC display-AHB reference through the pinned native
  Clock protocol, with bounded read/identity/Guard checks.
- Does NOT call the experimental non-GDSC child clock or rail reader.
- Holds the reference through the shared UEFI UI owner and uses the
  preexisting typed display Stop callback for exact reference decrement.
- Refuses retained or uncertain acquisition; only a proved no-side-effect
  refusal can be represented as display absent.
- Does not directly write MMIO registers, alter the GOP's framebuffer layout,
  switch boot slots, or flash persistent device storage.

The native clock enable can affect physical hardware. This remains an
INCOMPLETE_NOT_RELEASE experiment, has not been physically validated, and
is NOT evidence of repaired panel scanout. Keep this branch separate from
the known boot image. Review the binary and recovery plan before any
temporary physical boot. Do not install or flash this diagnostic.

Host tests use the actual coordinator and Owners manager with controlled
native boundaries; GCC-only success and exact cleanup, partial failure
retention and clean absence are checked. These are not hardware observations.
