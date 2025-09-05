import React, {useEffect,useState} from "react";
import axios from "axios"

import './App.css';

function App() {
  const [employees,setEmployees]=useState([]);
  const[name,setName]=useState("");
  const[role,setRole]=useState("");
  const[editId,setEditId]=useState(null);

  useEffect(() =>{
    fetchEmployees();
  },[]);

  const fetchEmployees=() =>{
    axios.get("http://34.58.102.85/employee").then(res=>setEmployees(res.data)).catch(err=>console.error(err));
  };

  const handleSubmit=(e) => {
    e.preventDefault();
    if(editId){
      axios.put(`http://34.58.102.85/employee/${editId}`,{name,role}).then(()=>{
        fetchEmployees();
        resetForm();
      });
    }
    else{
      axios.post("http://34.58.102.85/employee", { name, role })
        .then(() => {
          fetchEmployees();
          resetForm();
        });

    }
    }
  

  const handleDelete=(id)=>{
    axios.delete(`http://34.58.102.85/employee/${id}`).then(()=>fetchEmployees())
  };

  const handleEdit =(emp)=>{
    setName(emp.name);
    setRole(emp.role);
    setEditId(emp.id);
  };

  const resetForm =() =>{
    setName("");
    setRole("");
    setEditId(null);
    
  }


  return (
<div className="Container">
  <div  className="uppercontainer">
  <div className="uppercontainer-title">
    <h1>Employee Manager</h1>
  </div>
  <form className="uppercontainer-form" onSubmit={handleSubmit}>
    
    <div><input className="form-name" type="text" placeholder="Name" value={name} onChange={(e)=>setName(e.target.value)} required>
    </input></div>
    <div><input className="form-role" type="text" placeholder="Role" value={role} onChange={(e)=>setRole(e.target.value)} required>
    </input></div>
    <div><button className="form-button" type="Submit"> {editId? "Update":"Add"} </button></div>

  </form>
</div>
<hr/>
  <div className="lowercontainer">
    <div className="lowercontainer-title">
  <h2> All Employees</h2>
  </div>
  <div className="lowercontainer-body">
  <ul>
    {
      employees.map(emp=>(
        <li key={emp.id}>
          <div className="lowercontainer-name"><span>{emp.name} -{emp.role}</span></div>
          <div className="lowercontainer-buttons"><span>
            <button className="edit" onClick={()=> handleEdit(emp)}>Edit</button>
            <button className="delete" onClick={()=> handleDelete(emp.id)}>Delete</button>
          </span>
          </div>
        </li>
      ))
    }
  </ul>
  </div>
</div>
</div>
  );
}

export default App;
