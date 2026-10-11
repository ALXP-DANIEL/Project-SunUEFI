// SPDX-License-Identifier: BSD-2-Clause-Patent
#pragma once
#include <Uefi.h>
#include <Protocol/GraphicsOutput.h>

typedef BOOLEAN (EFIAPI *PIANO_PRODUCT_BOOT_LOG_ALIVE)(VOID);

// A display-only sink for actual initialization results. The caller owns the
// ExitBootServices fence and elapsed-time measurement. No console state changes.
EFI_STATUS PianoProductBootLogInitialize(EFI_GRAPHICS_OUTPUT_PROTOCOL *Gop,
                                        PIANO_PRODUCT_BOOT_LOG_ALIVE Alive);
// Fixed rows: DISPLAY, PAYLOAD, SMEM, INPUT, UFS, USB, MENU. Non-success results
// except NOT_STARTED show their complete native EFI_STATUS value. A display failure never becomes a
// service result; the caller continues to own all existing startup decisions.
EFI_STATUS PianoProductBootLogStage(CONST CHAR8 *Name,EFI_STATUS Status,
                                   UINT64 ElapsedMs);

// Experimental visual-only stage probe. Ten distinct solid colors and six
// large binary tiles (least significant bit at left) identify the last GOP
// Blt attempt even when USB service/RAM logs become unavailable. Index 1..63
// denotes the actual native StartImage sequence, not a hardcoded driver list.
// No SetMode, framebuffer pointer writes, console or hardware clock operations.
typedef enum {
  PianoProbeBeforeFoundation=0,
  PianoProbeBeforeNative=1,
  PianoProbeAfterNative=2,
  PianoProbeAfterFoundation=3,
  PianoProbeAfterUfs=4,
  PianoProbeAfterUsb=5,
  PianoProbeBeforeMenu=6,
  PianoProbeImmediatelyBeforeStartImage=7,
  PianoProbeImmediatelyAfterStartImage=8,
  PianoProbeAfterPostObserver=9
} PIANO_PRODUCT_VISUAL_PHASE;
EFI_STATUS PianoProductBootLogVisualProbe(PIANO_PRODUCT_VISUAL_PHASE Phase,UINT32 NativeIndex);
// Bounded visible native name on the current colored probe, not a console
// operation or an authoritative physical-scanout assertion.
EFI_STATUS PianoProductBootLogVisualLabel(CONST CHAR8 *Name);
