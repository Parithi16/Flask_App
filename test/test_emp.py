import unittest
from emp import cal_emp_salary

class Testemp(unittest.TestCase):
    def test_salary(self):
        self.assertEqual(cal_emp_salary(100,10),1210)
    
    def test_salary_error(self):
        self.assertRaises(ValueError,cal_emp_salary,-1,10)

if __name__==   "__main__":
    unittest.main()
