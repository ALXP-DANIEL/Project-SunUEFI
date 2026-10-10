# SPDX-License-Identifier: BSD-2-Clause-Patent
"""Host-only identity/APPv1 checks for the experimental PianoBoot payload."""
import hashlib
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from product_application import EXPECTED_SHA256, payload_for, selected, verify_payload
from product_contract import validate, validate_build_manifest
import json


class HostedPianoBootTest(unittest.TestCase):
    def test_real_application_identity(self):
        path, header, identity = selected(ROOT)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), EXPECTED_SHA256)
        self.assertEqual(identity["app_bytes"], 28672)
        self.assertIn("PIANO_PRODUCT_SIMPLEINIT_BYTES 28672U", header)

    def test_complete_app_payload(self):
        path, _, _ = selected(ROOT)
        raw = path.read_bytes()
        payload = payload_for(raw)
        self.assertEqual(len(payload), 28736)
        self.assertTrue(verify_payload(raw, payload))

    def test_fail_closed_wrong_app_or_payload(self):
        path, _, _ = selected(ROOT)
        raw = path.read_bytes()
        payload = bytearray(payload_for(raw))
        payload[12] ^= 1
        with self.assertRaises(ValueError):
            verify_payload(raw, payload)
        payload = bytearray(payload_for(raw))
        payload[-1] ^= 1
        with self.assertRaises(ValueError):
            verify_payload(raw, payload)
        with self.assertRaises(ValueError):
            verify_payload(raw[:-1], payload_for(raw))

    def test_experimental_policy_requires_pinned_app(self):
        policy=validate(json.loads((ROOT / "config/piano-product.json").read_text()))
        manifest={"target":"product","artifact":"PianoUEFI-product.img",
                  "features":policy["features"],"shared_core":True,
                  "fastboot_mode":"resident_background","fastboot_surfaces":policy["fastboot"]["available_in"],
                  "default_application":"PianoBoot","setup_key":"F12",
                  "diagnostic_reboot_timer":False,"backend_initialization_required":True,
                  "hosted_pianoboot":{"sha256":EXPECTED_SHA256,"device_validated":False}}
        self.assertEqual(validate_build_manifest(policy,manifest),manifest)
        manifest["hosted_pianoboot"]["sha256"]="0"*64
        with self.assertRaises(ValueError):
            validate_build_manifest(policy,manifest)


if __name__ == "__main__":
    unittest.main()
