import unittest
from analysis import estimate
class AnalysisTest(unittest.TestCase):
 def test_pair(self):
  rows=[{'player_id':'1','date':'2024-01-01','rest_day':'1','performance':'5'},{'player_id':'1','date':'2024-01-02','rest_day':'0','performance':'3'}]
  self.assertEqual(estimate(rows,iterations=100)['mean_difference'],2)
