from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import time
import os
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from flask_cors import CORS


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI", db_url)

db = SQLAlchemy(app)

def wait_for_db():
    connected = False
    while not connected:
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
            print("Database connection established!")
            connected = True
        except Exception as e:
            print(" DB connection failed:", repr(e))
            time.sleep(5)

wait_for_db()

class Employee(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(25),nullable=False)
    role=db.Column(db.String(10),nullable=False)

    def to_dict(self):
        return {"id":self.id,"name":self.name,"role":self.role}

with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully!")
    except OperationalError:
        print("Could not create tables. Check DB connection.")
        
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error":"Route not found"}),404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error":"Bad request"}),400

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error":"Internal Server Error"}),500


@app.route('/employee',methods=['POST'])
def add_employee():
    try:
        data=request.get_json()

        if not data or not data.get("name") or not data.get("role"):
            return jsonify({"error":"Bad request"}),400
        
        if not isinstance(data["name"],str):
            return jsonify({"error": "Bad request", "details": "Name must be a string"}), 400
        
        new_emp=Employee(name=data["name"],role=data["role"])
        db.session.add(new_emp)
        db.session.commit()
        return jsonify({"message":"employee added", "employee":new_emp.to_dict()}),201
    
    except Exception as e:
        return jsonify({"error": "Something went wrong" ,"details":str(e)}),400

@app.route('/employee', methods=['GET'])
def get_emp():
    employees=Employee.query.all()
    return jsonify([emp.to_dict() for emp in employees])

@app.route('/employee/<int:id>',methods=['GET'])
def get_empid(id):
    try:
        emp=Employee.query.get(id)
        if emp:
            return jsonify(emp.to_dict())
        else:
            return jsonify({"error": "Employee not found"}), 404

    except Exception as e:
        return jsonify({"error":str(e)}),404
    
@app.route('/employee/<int:id>', methods=['PUT'])
def update_emp(id):
    try:
        emp=Employee.query.get(id)
        if not emp:
            return jsonify({"error":"Employee Not Found"}),404
        
        data= request.get_json()
        emp.name=data.get("name", emp.name)
        emp.role=data.get("role",emp.role)
        db.session.commit()
        return jsonify({"message":"employee updated", "employee":emp.to_dict()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@app.route('/employee/<int:id>', methods=['DELETE'])
def delete_emp(id):
    emp=Employee.query.get(id)
    if not emp:
        return jsonify({"error":"Employee not found"}),404
    
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message":"Employee deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")
    app.run(host="0.0.0.0", port=5000, debug=False)



