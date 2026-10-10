#!/usr/bin/env python3
"""Exact, fail-closed identity for the PianoBoot APPv1 experiment.

The pinned SimpleInit source is still built and sealed independently; this
module deliberately selects the separate, prebuilt PianoBoot EFI application
for the product's runtime APPv1 payload.
"""
import hashlib
from pathlib import Path
import struct

from product_payload_digest import digest_header

RELATIVE = Path("uefi/applications/PianoBoot.efi")
EXPECTED_SHA256 = "c95e79c1b235ae1b8b91d29db66ef4e873cf6f477a19f8434ce59e2794460d9d"
MAGIC = b"SUNUEFI-APPv1\0".ljust(16, b"\0")


def selected(root):
    path = Path(root) / RELATIVE
    if path.is_symlink() or not path.is_file():
        raise ValueError("Expected regular pinned PianoBoot EFI application")
    header, identity = digest_header(path)
    if identity["sha256"] != EXPECTED_SHA256:
        raise ValueError("PianoBoot application identity changed")
    return path, header.replace("real built SimpleInit.efi",
                                "pinned independently built PianoBoot.efi; legacy macro ABI"), identity


def payload_for(raw):
    return struct.pack("<16sIIQ32s", MAGIC, 1, 64, len(raw),
                       hashlib.sha256(raw).digest()) + raw


def verify_payload(raw, payload):
    if len(payload) < 64:
        raise ValueError("Truncated APPv1 header")
    magic, version, header, size, digest = struct.unpack_from("<16sIIQ32s", payload)
    if (magic, version, header, size) != (MAGIC, 1, 64, len(raw)):
        raise ValueError("Invalid APPv1 layout")
    if payload[64:] != raw or digest != hashlib.sha256(raw).digest():
        raise ValueError("APPv1 content or digest mismatch")
    return True
