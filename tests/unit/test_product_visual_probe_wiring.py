"""Source wiring guard for the isolated visual-only regression experiment."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


class ProductVisualProbeWiring(unittest.TestCase):
    def test_build_flag_and_exact_order(self):
        prep=(ROOT/'tools/prepare_product.py').read_text()
        package=(ROOT/'tools/package_product.py').read_text()
        core=(ROOT/'uefi/core/PianoProductCore.c').read_text()
        self.assertIn("'PIANO_EXPERIMENT_DISPLAY_PHASE_PROBE=1'",prep)
        self.assertIn("prepared.get('visual_phase_probe')!=VISUAL_PHASE_PROBE",package)
        self.assertIn('product_dsc.count',package)
        self.assertIn('core_make',package)
        self.assertIn('#ifdef PIANO_EXPERIMENT_DISPLAY_PHASE_PROBE',core)
        self.assertNotIn('PIANO_EXPERIMENT_GCC_AHB_ONLY',core)
        self.assertLess(core.index('VisualProbe(PianoProbeBeforeFoundation,NULL,3500000)'),
                        core.index('PianoProbeFoundation();'))
        self.assertLess(core.index('PianoProbeFoundation();'),
                        core.index('VisualProbe(PianoProbeAfterFoundation,NULL,3500000)'))
        self.assertLess(core.index('VisualProbe(PianoProbeAfterFoundation,NULL,3500000)'),
                        core.index('PianoUfsSetProbeAction(InitUfs)'))
        self.assertLess(core.index('PianoUfsSetProbeAction(InitUfs)'),
                        core.index('VisualProbe(PianoProbeAfterUfs,NULL,1000000)'))
        self.assertLess(core.index('PianoUsbControllerServiceStart(Fdt,&UsbConfig)'),
                        core.index('VisualProbe(PianoProbeAfterUsb,NULL,500000)'))
        self.assertLess(core.index('VisualProbe(PianoProbeBeforeMenu,NULL,1000000)'),
                        core.index('PianoBootPolicyInitialize(Image)'))
        self.assertIn('VisualProbe(Before?PianoProbeBeforeNative:PianoProbeAfterNative,Name,500000)',core)
        self.assertIn('mVisualNativeIndex<63',core)
        native=(ROOT/'uefi/core/NativeProbe.c').read_text()
        self.assertIn('PianoNativeSetLaunchObserver(ObserveLaunchBoundary);',core)
        self.assertIn('PianoNativeSetLaunchObserver(NULL);',core)
        self.assertIn('AsciiStrCmp(Name,"HALIOMMU")==0',core)
        self.assertIn('PianoProbeImmediatelyBeforeStartImage',core)
        self.assertIn('PianoProbeImmediatelyAfterStartImage',core)
        self.assertIn('mVisualNativeIndex==13',core)
        self.assertIn('PianoProductBootLogVisualLabel(NativeName)',core)
        self.assertIn('PianoProbeAfterPostObserver',core)
        self.assertIn('mVisualNativeIndex==13))',core)
        self.assertLess(native.index('if(mNativeObserver)mNativeObserver(Image->Name,TRUE);'),
                        native.index('if(mNativeLaunchObserver)mNativeLaunchObserver(Image->Name,TRUE);'))
        self.assertLess(native.index('if(mNativeLaunchObserver)mNativeLaunchObserver(Image->Name,TRUE);'),
                        native.index('Status=gBS->StartImage(Handle,NULL,NULL);'))
        self.assertLess(native.index('Status=gBS->StartImage(Handle,NULL,NULL);'),
                        native.index('if(mNativeLaunchObserver)mNativeLaunchObserver(Image->Name,FALSE);'))
        self.assertLess(native.index('if(mNativeLaunchObserver)mNativeLaunchObserver(Image->Name,FALSE);'),
                        native.index('if(mNativeObserver)mNativeObserver(Image->Name,FALSE);'))

    def test_gop_only_no_modeset_or_mmio(self):
        log=(ROOT/'uefi/core/PianoProductBootLog.c').read_text()
        fn=log.split('EFI_STATUS PianoProductBootLogVisualProbe(',1)[1]
        for forbidden in ('SetMode(', 'Mmio', 'ResetSystem(', 'FrameBufferBase',
                          'SetMemorySpaceAttributes', 'GetMemorySpaceDescriptor'):
            self.assertNotIn(forbidden,fn)
        self.assertIn('NativeIndex>63',fn)
        self.assertIn('mCanvas.Gop->Blt',log)


if __name__=='__main__':
    unittest.main()
