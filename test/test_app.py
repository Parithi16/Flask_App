import json,unittest
from backend.app import app,db,Employee

class EmployeeTest(unittest.TestCase):

    def setUp(self):
        
        app.config['TESTING']=True
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///:memory:'
        self.app=app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_emp(self):
        response=self.app.post('/employee', json={"name":"Parithi","role":"Tester"})
        self.assertEqual(response.status_code, 201)
        data=json.loads(response.data)
        self.assertEqual("employee added",data["message"])

        response=self.app.post('/employee', json={"name":"Parithi"})
        self.assertEqual(response.status_code, 400)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Bad request") 

        
        response=self.app.post('/employee', json={"name":123 ,"role":"Tester"})
        self.assertEqual(response.status_code, 400)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Bad request")
        self.assertIn("details",data)
        self.assertIsInstance(data["details"],str) 

    
    def test_get_employee(self):
        with app.app_context():
            emp=Employee(name="Bob",role="Engineer")
            db.session.add(emp)
            db.session.commit()
            emp_id=emp.id
        
        #proper request
        response=self.app.get(f"/employee/{emp_id}")
        self.assertEqual(response.status_code,200)
        data=json.loads(response.data)
        self.assertEqual("Bob",data["name"])
        self.assertEqual("Engineer",data["role"])

        #employee not found
        response=self.app.get(f"/employee/{emp_id+10}")
        self.assertEqual(response.status_code,404)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Employee not found") 

        #user id as string format (Route Not found)
        response=self.app.get("/employee/emp_id")
        self.assertEqual(response.status_code,404)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Route not found") 

        

    def test_del_employee(self):
        with app.app_context():
            emp=Employee(name="Bob",role="Engineer")
            db.session.add(emp)
            db.session.commit()
            emp_id=emp.id
        
        response=self.app.delete(f"/employee/{emp_id}")
        self.assertEqual(response.status_code,200)
        data=json.loads(response.data)
        self.assertEqual("Employee deleted",data["message"])

        response=self.app.delete(f"/employee/{emp_id+10}")
        self.assertEqual(response.status_code,404)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Employee not found") 

        response=self.app.delete("/employee/emp_id+10")
        self.assertEqual(response.status_code,404)
        data=json.loads(response.data)
        self.assertIn("error",data)
        self.assertEqual(data["error"], "Route not found") 


if __name__ =="__main__":
    unittest.main()