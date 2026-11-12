"""Mutation fixtures block mistaken status promotion or unsafe review behavior."""
import importlib.util
from pathlib import Path
import shutil,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review',ROOT/'scripts/verify_identity_workbench.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='gc-review-workbench-')
        self.addCleanup(self.tmp.cleanup)
        old=mod.SITE
        self.site=Path(self.tmp.name)/'site'
        (self.site/'identity-review').mkdir(parents=True)
        (self.site/'assets').mkdir(parents=True)
        shutil.copy2(old/'identity-review/index.html',self.site/'identity-review/index.html')
        shutil.copy2(old/'assets/identity-workbench.js',self.site/'assets/identity-workbench.js')
        mod.SITE=self.site
        self.addCleanup(lambda:setattr(mod,'SITE',old))
    def replace(self,fragment,replacement,filename='identity-review/index.html'):
        p=self.site/filename
        text=p.read_text()
        self.assertIn(fragment,text)
        p.write_text(text.replace(fragment,replacement,1))
    def test_original(self):
        self.assertEqual(mod.audit(),[])
    def test_promotion_rejected(self):
        self.replace('data-review-status="candidate"','data-review-status="official"')
        self.assertTrue(any('promoted' in x for x in mod.audit()))
    def test_wrong_role_rejected(self):
        self.replace('data-review-category="pillars"','data-review-category="applications"')
        self.assertTrue(any('grouping' in x for x in mod.audit()))
    def test_missing_link_rejected(self):
        self.replace('href="#identity-goreeshield"','href="#unlinked-goreeshield"')
        self.assertTrue(any('permalink' in x for x in mod.audit()))
    def test_untrusted_network_code_rejected(self):
        p=self.site/'assets/identity-workbench.js'
        p.write_text(p.read_text()+'\nfetch("https://example.invalid/tracker");')
        self.assertTrue(any('data/network' in x for x in mod.audit()))
    def test_accessibility_status_rejected(self):
        self.replace('role="status" aria-live="polite"','role="status" aria-live="off"')
        self.assertTrue(any('announcement' in x for x in mod.audit()))
if __name__=='__main__':unittest.main()
