import tempfile,unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_task_report(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3';app.add('Finish README','Portfolio','Ada','2026-11-01','todo',p);self.assertEqual(app.report(p)['tasks'],1)
if __name__=='__main__':unittest.main()
