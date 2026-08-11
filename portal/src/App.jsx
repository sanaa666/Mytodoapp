import { Header } from './components/Header';
import AddButton from './components/AddButton';
import TasksContainer from './components/TasksContainer';
import FilterButtons from './components/FilterButtons';
import Input from './components/Input';
import ClearButton from './components/ClearButton';
import './index.css'
import { useState, useEffect } from 'react';

function ToDo() {

  const [username, setUsername] = useState("");
  const [usernameInput, setUsernameInput] = useState("");
  const [userId, setUserId] = useState(null)
  const [tasks, setTasks] = useState([]);

  const [newTask, setNewTask] = useState("");
  const [filter, setFilter] = useState("all");
  const [editingId, setEditingId] = useState(null);
  const [editText, setEditText] = useState("");
  const [loading, setLoading] = useState(true);

  const handleChange = (e) => {
    const value = e.target.value
    setUsernameInput(value)
  }

  const onDoubleClickHandler = () => {
    setEditingId(null);
    setEditText("");
  }

  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (!savedUser) {
      setLoading(false);
      return;
    }

    const user = JSON.parse(savedUser);

    setUsername(user.username);
    setUserId(user.userId);
  }, []);

  useEffect(() => {
    if (!userId) return;

    fetch(`${import.meta.env.VITE_API_URL}/todos?user_id=${userId}`)
      .then(res => {
        if (!res.ok) throw new Error("User not found");
        return res.json();
      })
      .then(data => {
        setTasks(data);
        setLoading(false)
      })
      .catch(err => {
        console.log(err);
        setTasks([]);
        setLoading(false);
      });
  }, [userId]);

  if (!username) {
    return (
      <div className="enter-container">
        <h2> Username: </h2>
        <div className='username-form'>
          <input
            placeholder='Enter a username...'
            className="username-input"
            value={usernameInput.toLowerCase()}
            onChange={handleChange}
          />


          <button
            className="continue-button"
            onClick={async () => {
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
                const user = await response.json();

                setUsername(user.username);
                setUserId(user.id);

                localStorage.setItem(
                  "user",
                  JSON.stringify({
                    username: user.username,
                    userId: user.id
                  })
                )
              }
            }}
          >
            Continue
          </button>
        </div>
      </div >
    );
  }

  const incompleteCount = tasks.filter(task => !task.completed).length;

  function handleInputChange(event) {
    setNewTask(event.target.value);
  }


  async function addItem() {
    if (newTask.trim() === "") return;


    console.log("USER ID:", userId);
    console.log("NEW TASK:", newTask);

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/todos?user_id=${userId}`,
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

    const data = await response.json();
    console.log("STATUS:", response.status);

    console.log("RESPONSE:", data);


    if (!response.ok) {
      console.log("ERROR:", data);
      return;
    }

    setTasks(t => [...t, data]);
    setNewTask("");

  }

  async function completeTask(id) {

    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/todos?user_id=${userId}&todo_id=${id}`,
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
      `${import.meta.env.VITE_API_URL}/todos?user_id=${userId}&todo_id=${id}`,
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

    const response = await fetch(`${import.meta.env.VITE_API_URL}/todos?user_id=${userId}&todo_id=${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",

      },
      body: JSON.stringify({
        text: editText,
        completed: todo.completed,
      })
    }
    );

    const updatedTodo = await response.json();

    setTasks(tasks.map(task =>
      task.id === id ? updatedTodo : task
    )
    );

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
      <h1>{username}'s Todos</h1>
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
      <button
        className="logout-button"
        onClick={() => {
          localStorage.removeItem("user");
          setUsername("");
          setUsernameInput("");
          setUserId(null);
          setTasks([]);
        }}
      >
        Log out
      </button>
    </div >

  );
}
export default ToDo
