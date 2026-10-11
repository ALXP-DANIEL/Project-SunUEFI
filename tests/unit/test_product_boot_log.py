"""Execute the actual native product boot log renderer, no device operations."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
_include_candidates = (
    ROOT / 'upstream/Mu-Silicium/Mu_Basecore/MdePkg/Include',
    ROOT.parent / 'sunuefi-dependencies/Mu-Silicium/Mu_Basecore/MdePkg/Include',
)
INC = next((path for path in _include_candidates if (path / 'Uefi.h').is_file()), _include_candidates[0])
SOURCE = ROOT / 'uefi/core/PianoProductBootLog.c'
SPLASH = ROOT / 'uefi/components/product-support/Library/ProductBootManagerLib/ProductSplash.c'


class ProductBootLogTests(unittest.TestCase):
    def test_actual_pixels_status_elapsed_and_failure_fences(self):
        output = ROOT / 'build/previews/product-splash'
        output.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='piano-bootlog-') as directory:
            executable = Path(directory) / 'bootlog'
            host_flags = ['-fno-pie', '-no-pie'] if sys.platform.startswith('linux') else []
            subprocess.run(['cc', '-std=gnu11', '-Wall', '-Wextra', '-Werror',
                '-Wno-misleading-indentation', '-fshort-wchar', '-fsanitize=address,undefined',
                *host_flags, '-I' + str(INC), '-I' + str(INC / 'X64'),
                str(ROOT / 'tests/native/PianoProductBootLogTest.c'), str(SOURCE), str(SPLASH),
                '-o', str(executable)], check=True)
            asan_options = 'detect_leaks=1' if sys.platform.startswith('linux') else 'detect_leaks=0'
            run = subprocess.run([str(executable), str(output / 'product-bootlog-3200x2136.ppm')],
                capture_output=True, text=True, env={**os.environ, 'ASAN_OPTIONS': asan_options})
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            print(run.stdout.strip())
        subprocess.run([str(ROOT / 'build/host-tools/usr/bin/clang'),
            '--target=aarch64-windows-msvc', '-ffreestanding', '-fshort-wchar',
            '-fsyntax-only', '-Wall', '-Wextra', '-Werror', '-I' + str(INC),
            '-I' + str(INC / 'AArch64'), str(SOURCE)], check=True)


if __name__ == '__main__':
    unittest.main()
