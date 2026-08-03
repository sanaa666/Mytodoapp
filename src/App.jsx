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
  const[editingIndex, setEditingIndex] = useState(null);
  const[editText, setEditText] = useState("");
  
  const [key, setKey] = useState('');
  const keyDown = event => {
    setKey(event.key);
  };


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
            editingIndex={editingIndex}
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
