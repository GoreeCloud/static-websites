"""Negative acceptance fixtures: no official promotion, external assets or tampered SVG."""
from pathlib import Path
import importlib.util, json, shutil, tempfile, unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('gallery',ROOT/'scripts/verify_identity_review_gallery.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class IdentityReviewGalleryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gc-identity-review-')
        self.addCleanup(self.temp.cleanup)
        folder=Path(self.temp.name)
        source=mod.SITE
        self.site=folder/'site'
        (self.site/'assets').mkdir(parents=True)
        shutil.copytree(source/'assets/identity-review',self.site/'assets/identity-review')
        (self.site/'identity-review').mkdir()
        (self.site/'products').mkdir()
        shutil.copy2(source/'identity-review/index.html',self.site/'identity-review/index.html')
        shutil.copy2(source/'products/index.html',self.site/'products/index.html')
        self.manifest=folder/'manifest.json'
        shutil.copy2(mod.MANIFEST,self.manifest)
        old_site,old_manifest=mod.SITE,mod.MANIFEST
        mod.SITE=self.site
        mod.MANIFEST=self.manifest
        self.addCleanup(lambda:setattr(mod,'SITE',old_site))
        self.addCleanup(lambda:setattr(mod,'MANIFEST',old_manifest))

    def test_original_passes(self):
        self.assertEqual(mod.audit(),[])

    def test_modified_svg_is_rejected(self):
        p=self.site/'assets/identity-review/wardveil/app-icon.svg'
        p.write_bytes(p.read_bytes()+b'<!-- altered -->')
        self.assertTrue(any('Byte mismatch' in x for x in mod.audit()))

    def test_candidate_marked_official_is_rejected(self):
        p=self.site/'identity-review/index.html'
        p.write_text(p.read_text().replace('data-review-status="candidate"',
                           'data-review-status="official"',1))
        self.assertTrue(any('wrong candidate count' in x for x in mod.audit()))

    def test_source_commit_drift_is_rejected(self):
        data=json.loads(self.manifest.read_text())
        data['source_commit']='0'*40
        self.manifest.write_text(json.dumps(data))
        self.assertTrue(any('Unreviewed source commit' in x for x in mod.audit()))

    def test_tampered_16px_pixel_image_is_rejected(self):
        p=self.site/'assets/identity-review/mesh/icon-16.png'
        p.write_bytes(p.read_bytes()[:-4])
        self.assertTrue(any('Byte mismatch' in x for x in mod.audit()))

    def test_missing_review_notice_is_rejected(self):
        p=self.site/'identity-review/index.html'
        p.write_text(p.read_text().replace('These designs have not been approved as official brands.',
                            'These designs are approved.',1))
        self.assertTrue(any('Review-only disclosure missing' in x for x in mod.audit()))

    def test_unexpected_extra_file_in_manifest_is_rejected(self):
        data=json.loads(self.manifest.read_text())
        data['files'].append(dict(data['files'][0]))
        self.manifest.write_text(json.dumps(data))
        self.assertTrue(any('Missing or extra imported' in x for x in mod.audit()))

if __name__=='__main__':unittest.main()
