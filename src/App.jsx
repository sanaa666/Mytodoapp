import './index.css'
import {useState} from 'react';

function ToDo(){
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState("");

  const incompleteCount = tasks.filter(task => !task.completed).length;

  function handleInputChange(event){
    setNewTask(event.target.value);
  }

  
  function addItem(){
      setTasks(t=> [...t, {text: newTask, completed:false}]);
      setNewTask("")

  }

  function completeTask(index){
    setTasks(tasks.map((task, i)=>
      i === index ? {...task, completed: !task.completed} : task
    ));

 

  }

  function deleteTask(index){
    const updatedTasks = tasks.filter((element, i) => i !== index);
    setTasks(updatedTasks);
  }


  return(
    
          <div className="task">
            <h1>To Do</h1>
            <h3>Items still not completed: {incompleteCount}</h3>
            <div>
              <input
                      type="text"
                      placeholder="Enter task..."
                      className="task-enter"
                      value={newTask}
                      onChange={handleInputChange}/>
                    <button
                      className="add-button"
                      onClick={addItem}>
                      Add
                    </button>
            </div>

            <ol>
              {tasks.map((task, index)=>
                <li key={index}>
                  <span className={`text ${task.completed ?  "completed" : ""}`}>
                    {task.text}
                  </span>
                  <button
                    className="complete-button"
                    onClick= {() => completeTask(index)}>
                    ✅
                  </button>
                  <button
                    className="delete-button"
                    onClick= {() => deleteTask(index)}>
                    Delete
                  </button>

                </li>
              )}
            </ol>

  
          
          </div>);

}

export default ToDo