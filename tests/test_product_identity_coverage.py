"""Regression tests prevent replacing missing marks with fake 'official' assets."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("brand_coverage",ROOT/"scripts/verify_product_identity_coverage.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ProductIdentityAudit(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gc-product-icons-')
        self.addCleanup(self.temp.cleanup)
        self.orig_site=module.SITE
        self.site=Path(self.temp.name)/'site'
        (self.site/'products').mkdir(parents=True)
        (self.site/'assets/product-icons').mkdir(parents=True)
        shutil.copy2(self.orig_site/'products/index.html',self.site/'products/index.html')
        for path in (self.orig_site/'assets/product-icons').iterdir():
            shutil.copy2(path,self.site/'assets/product-icons'/path.name)
        module.SITE=self.site
        self.addCleanup(lambda:setattr(module,'SITE',self.orig_site))

    def change(self,old,new):
        p=self.site/'products/index.html'
        t=p.read_text()
        self.assertIn(old,t)
        p.write_text(t.replace(old,new,1))

    def test_verified_site(self):
        self.assertEqual(module.audit(),[])

    def test_tampered_browser_master(self):
        p=self.site/'assets/product-icons/browser-family.svg'
        p.write_bytes(p.read_bytes()+b'<!-- unauthorized -->')
        self.assertTrue(any('source icon changed' in x for x in module.audit()))

    def test_missing_pillar_promoted_falsely(self):
        self.change('data-identity-status="missing"','data-identity-status="official"')
        self.assertTrue(any('status' in x for x in module.audit()))

    def test_candidate_promoted_without_approval(self):
        self.change('data-identity-status="candidate"','data-identity-status="official"')
        self.assertTrue(any('status' in x for x in module.audit()))

    def test_drive_consumer_promoted_without_central_approval(self):
        self.change('data-identity-status="existing-consumer"','data-identity-status="official"')
        self.assertTrue(any('status' in x for x in module.audit()))

    def test_missing_exact_source_file(self):
        (self.site/'assets/product-icons/search.svg').unlink()
        self.assertTrue(any('source icon changed' in x for x in module.audit()))

    def test_no_accidental_external_mark(self):
        self.change('/assets/product-icons/browser-family.svg','https://unverified.example/logo.svg')
        self.assertTrue(any('wrong product icon' in x for x in module.audit()))

if __name__=='__main__':
    unittest.main()
