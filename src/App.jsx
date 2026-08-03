import './index.css'
import {useState, useEffect} from 'react';

function ToDo(){
  const [tasks, setTasks] = useState(()=>{
    const savedTasks = localStorage.getItem("tasks");
    return savedTasks ? JSON.parse(savedTasks) : [];
  });

  const [newTask, setNewTask] = useState("");
  const [filter, setFilter] = useState("all");
  const[editingIndex, setEditingIndex] = useState(null);
  const[editText, setEditText] = useState("");
  
  const onDoubleClickHandler = () => {
    setEditingIndex(null);
    setEditText("");
  }

  useEffect(()=>{
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }, [tasks]);   

  const incompleteCount = tasks.filter(task => !task.completed).length;

  function handleInputChange(event){
    setNewTask(event.target.value);
  }

  
  function addItem(){
      if (newTask.trim() === "") return;
      setTasks(t=> [...t, {text: newTask, completed:false, status: "in progress"}]);
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

  function startEditing(index, text){
    setEditingIndex(index);
    setEditText(text);
  }

  function saveEdit(index){
    if (editText.trim() === "") return;
    setTasks(tasks.map((task, i) =>
      i === index ? {...task, text: editText} : task
    ));
    setEditingIndex(null);
    setEditText("");
  }

  function cancelEdit(){
    setEditingIndex(null);
    setEditText("");
  }

  const displayedTasks = tasks.filter(task => {
    if (filter === "completed") {
      return task.completed;
    } else if (filter === "in progress") {  
      return !task.completed;
  
    } return true;
  });


  return(
    
          <div className="task">
            <h1>To Do</h1>
            <h3>Items still not complete: {incompleteCount}</h3>
            <button onClick={() => setTasks(tasks => tasks.filter(task => !task.completed))} className="clear-button">Clear All Completed</button>
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

 
          <div className="tasks-container">
            <ol>
                {displayedTasks.map((task, index)=>
                  <li key={index}>
                    {editingIndex === index ? (
                      <div>
                        <input
                          type="text"
                          value={editText}
                          onChange={(e) => setEditText(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter") saveEdit(index);
                            if (e.key === "Escape") cancelEdit();
                          }}
                        />

                      <button className="save-button" onClick={() => saveEdit(index)}>Save</button>
                      <button className="cancel-button" onClick={cancelEdit}>Cancel</button>
                      </div>
                    ) : (
                      <div>
                        
                      
                        <span className={`text ${task.completed ?  "completed" : ""}`}
                        onDoubleClick={() => startEditing(index, task.text)}
                        style={{cursor: "pointer"}}>
                          {task.text}
                        </span>

                          <button
                            className="complete-button"
                            onClick= {() => completeTask(index)}>
                            {task.completed ? "Undo" : "Done"}
                          </button>
                          <button
                            className="delete-button"
                            onClick= {() => deleteTask(index)}>
                            Delete
                          </button>
                      </div>

                    )}
                    
                  </li>
              )}
            </ol>
          </div>
          <div className="filter-buttons">
            <button onClick={() => setFilter("all")}>All</button>
            <button onClick={() => setFilter("completed")}>Completed</button>
            <button onClick={() => setFilter("in progress")}>Active</button>

          </div>
          </div>

  );
}
export default ToDo
