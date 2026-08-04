import { Header } from './components/Header';
import AddButton from './components/AddButton';
import TasksContainer from './components/TasksContainer';
import FilterButtons from './components/FilterButtons';
import Input from './components/Input';
import ClearButton from './components/ClearButton';
import './index.css'
import {useState, useEffect} from 'react';

function ToDo(){
  const [tasks, setTasks] = useState(()=> {
    const savedTasks = localStorage.getItem("tasks");
    return savedTasks ? JSON.parse(savedTasks) : [];
  });

  const [newTask, setNewTask] = useState("");
  const [filter, setFilter] = useState("all");
  const[editingId, setEditingId] = useState(null);
  const[editText, setEditText] = useState("");
  
  const [key, setKey] = useState('');
  const keyDown = event => {
    setKey(event.key);
  };


  const onDoubleClickHandler = () => {
    setEditingId(null);
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
      const newTaskObject={
        id: Date.now(),
        text: newTask,
        completed: false,
      }
      setTasks(t=> [...t, newTaskObject]);
      setNewTask("")

  }

  function completeTask(id){
    setTasks(tasks.map(task =>
      task.id === id ? {...task, completed: !task.completed} : task
    ));
  }

  function deleteTask(id){
    const updatedTasks = tasks.filter(task => task.id !== id);
    setTasks(updatedTasks);
  }

  function startEditing(id, text){
    setEditingId(id);
    setEditText(text);
  }

  function saveEdit(id){
    if (editText.trim() === "") return;
    setTasks(tasks.map(task =>
      task.id === id ? {...task, text: editText} : task
    ));
    setEditingId(null);
    setEditText("");
  }

  function cancelEdit(){
    setEditingId(null);
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
            <Header incompleteCount={incompleteCount} />
            <ClearButton setTasks={setTasks} />
            <div>
                      <Input
                        newTask={newTask}
                        handleInputChange={handleInputChange}
                        addItem={addItem}
                      /> 
                      <AddButton addItem={addItem} />
            </div>

 
          <TasksContainer
            displayedTasks={displayedTasks}
            editingId={editingId}
            editText={editText}
            setEditText={setEditText}
            startEditing={startEditing}
            saveEdit={saveEdit}
            cancelEdit={cancelEdit}
            completeTask={completeTask}
            deleteTask={deleteTask}
          />
          <FilterButtons setFilter={setFilter} />
          </div>

  );
}
export default ToDo
