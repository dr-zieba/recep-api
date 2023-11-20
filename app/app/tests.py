from django.test import SimpleTestCase
from app.calc import calc

class CalcTest(SimpleTestCase):
    def test_calc(self):
        res = calc(1,2)
        self.assertEquals(res, 3)