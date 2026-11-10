import io
import unittest
import zipfile
from src.cow_official_run import membership_csv

class OfficialSourceTests(unittest.TestCase):
    def make_zip(self, files):
        buf=io.BytesIO()
        with zipfile.ZipFile(buf,"w") as z:
            for name,body in files.items():
                z.writestr(name,body)
        return buf.getvalue()
    def test_extract_exact_member(self):
        blob=self.make_zip({"nested/system2024.csv":"CCode,Year\n2,1939\n","README.txt":"info"})
        data,name=membership_csv(blob)
        self.assertEqual(name,"nested/system2024.csv")
        self.assertIn(b"1939",data)
    def test_reject_ambiguous_members(self):
        blob=self.make_zip({"system2024.csv":"a","copy/system2024.csv":"b"})
        with self.assertRaises(ValueError):
            membership_csv(blob)
    def test_reject_missing_member(self):
        with self.assertRaises(ValueError):
            membership_csv(self.make_zip({"unrelated.csv":"x"}))

if __name__=="__main__":
    unittest.main()
