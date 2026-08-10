import { Header } from './components/Header';
import AddButton from './components/AddButton';
import TasksContainer from './components/TasksContainer';
import FilterButtons from './components/FilterButtons';
import Input from './components/Input';
import ClearButton from './components/ClearButton';
import './index.css'
import { useState, useEffect } from 'react';

function ToDo() {

  console.log("API URL:", import.meta.env.VITE_API_URL);
  const [username, setUsername] = useState("");
  const [usernameInput, setUsernameInput] = useState("");
  const [tasks, setTasks] = useState([]);

  const [newTask, setNewTask] = useState("");
  const [filter, setFilter] = useState("all");
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState("");
  const [loading, setLoading] = useState(true);



  const onDoubleClickHandler = () => {
    setEditingId(null);
    setEditText("");
  }

  useEffect(() => {
    if (!username) return;

    console.log("USERNAME:", username);
    fetch(`${import.meta.env.VITE_API_URL}/todos?username=${username}`)
      .then(res => res.json())
      .then(data => {
        console.log(data);
        setTasks(data);
        setLoading(false)
      });
  }, [username]);

  if (!username) {
    return (
      <div>
        <h2> Enter your username: </h2>
        <input
          value={usernameInput}
          onChange={(e) => setUsernameInput(e.target.value)}
        />

        <button onClick={async () => {
          const response = await fetch(
            `${import.meta.env.VITE_API_URL}/users`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                username: usernameInput,
              }),
            }
          );

          if (response.ok) {
            setUsername(usernameInput);
          } else {
            setUsername(usernameInput);
          }
        }}
        >
          Continue
        </button>
      </div >
    );
  }

  const incompleteCount = tasks.filter(task => !task.completed).length;

  function handleInputChange(event) {
    setNewTask(event.target.value);
  }


  async function addItem() {
    if (newTask.trim() === "") return;

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/todos?username=${username}`,
      {
        method: "POST",
        headers: {
          "Content-type": "application/json",
        },
        body: JSON.stringify({
          text: newTask,
          completed: false,
        }),
      }
    );

    const createdTodo = await response.json();
    setTasks(t => [...t, createdTodo]);
    setNewTask("")

  }

  async function completeTask(id) {

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/todos/${id}?username=${username}`,
      {
        method: "PATCH",
      }
    );

    const updatedTodo = await response.json();

    setTasks(tasks => tasks.map(task =>
      task.id === id ? updatedTodo : task

    ));
  }

  async function deleteTask(id) {
    await fetch(
      `${import.meta.env.VITE_API_URL}/todos/${id}?username=${username}`,
      {
        method: "DELETE",
      }
    );
    setTasks(tasks.filter(task => task.id !== id));
  }

  function startEditing(id, text) {
    setEditingId(id);
    setEditText(text);
  }

  async function saveEdit(id) {
    if (editText.trim() === "") return;

    const todo = tasks.find(task => task.id === id);

    const response = await fetch(`${import.meta.env.VITE_API_URL}/todos/${id}?username=${username}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",

      },
      body: JSON.stringify({
        text: editText,
        completed: todo.completed,
      })
    });

    const updatedTodo = await response.json();

    setTasks(tasks.map(task =>
      task.id === id ? updatedTodo : task
    ));
    setEditingId(null);
    setEditText("");
  }

  function cancelEdit() {
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

  if (loading) {
    return <h2>Loading...</h2>;
  }


  return (
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
