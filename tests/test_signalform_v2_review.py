"""Fail-closed identity review fixtures: no tampering or unofficial promotion."""
from pathlib import Path
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sfv2',ROOT/'scripts/verify_signalform_v2_review.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class SignalformReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='sfv2-')
        self.addCleanup(self.tmp.cleanup)
        root=Path(self.tmp.name)
        src=mod.SITE
        self.site=root/'site'
        (self.site/'assets').mkdir(parents=True)
        shutil.copytree(src/'assets/identity-signalform-v2',self.site/'assets/identity-signalform-v2')
        (self.site/'identity-review-v2').mkdir()
        (self.site/'identity-review').mkdir()
        (self.site/'products').mkdir()
        for name in ['identity-review-v2/index.html','identity-review/index.html','products/index.html']:
            shutil.copy2(src/name,self.site/name)
        self.manifest=root/'manifest.json'
        shutil.copy2(mod.META,self.manifest)
        old_site,old_manifest=mod.SITE,mod.META
        mod.SITE=self.site
        mod.META=self.manifest
        self.addCleanup(lambda:setattr(mod,'SITE',old_site))
        self.addCleanup(lambda:setattr(mod,'META',old_manifest))

    def mutate(self,path,old,new):
        p=self.site/path
        text=p.read_text()
        self.assertIn(old,text)
        p.write_text(text.replace(old,new,1))

    def test_original_passes(self):
        self.assertEqual(mod.audit(),[])

    def test_tampered_icon_rejected(self):
        p=self.site/'assets/identity-signalform-v2/gateway/app-icon.svg'
        p.write_bytes(p.read_bytes()+b'<!-- tampered -->')
        self.assertTrue(any('SHA mismatch' in e for e in mod.audit()))

    def test_candidate_promotion_rejected(self):
        self.mutate('identity-review-v2/index.html','data-approval="pending"','data-approval="official"')
        self.assertTrue(any('approval state' in e for e in mod.audit()))

    def test_untrusted_source_commit_rejected(self):
        j=json.loads(self.manifest.read_text())
        j['source_commit']='0'*40
        self.manifest.write_text(json.dumps(j))
        self.assertTrue(any('source commit' in e for e in mod.audit()))

    def test_missing_v1_comparison_rejected(self):
        self.mutate('identity-review-v2/index.html','/assets/identity-review/mesh/app-icon.svg','/assets/nonexistent.svg')
        self.assertTrue(any('Foundation v1 comparison' in e for e in mod.audit()))

    def test_illicit_v2_in_products_rejected(self):
        p=self.site/'products/index.html'
        p.write_text(p.read_text()+'\n<a href="/identity-review-v2/">Replacement official logo</a>')
        self.assertTrue(any('Official Products catalog' in e for e in mod.audit()))

    def test_missing_disclosure_rejected(self):
        self.mutate('identity-review-v2/index.html','All seven designs are proposals.','All seven are approved.')
        self.assertTrue(any('disclosure absent' in e for e in mod.audit()))

    def test_missing_brand_source_file_rejected(self):
        (self.site/'assets/identity-signalform-v2/analytics/logo.svg').unlink()
        self.assertTrue(any('missing or symlink asset' in e for e in mod.audit()))

if __name__=='__main__':unittest.main()
