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
  const [passwordInput, setPasswordInput] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);

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

    fetch(`/todos?user_id=${userId}`)
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
        <h2> {isSignUp ? "Sign Up" : "Log In"} </h2>
        <div className='username-form'>
          <input
            placeholder='Username'
            className="username-input"
            value={usernameInput}
            onChange={(e) => setUsernameInput(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="password-input"
            value={passwordInput}
            onChange={(e) => setPasswordInput(e.target.value)}
          />



          <button
            className="continue-button"
            onClick={async () => {
              const cleanUsername = usernameInput.trim().toLowerCase();
              const cleanPassword = passwordInput.trim();

              if (!cleanUsername || !cleanPassword) return;


              const endpoint = isSignUp ? "/users" : "/login";
              try {


                const response = await fetch(endpoint,
                  {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                      username: cleanUsername,
                      password: cleanPassword,
                    }),
                  }
                );

                if (response.ok) {
                  const user = await response.json();
                  setUsername(user.username);
                  setUserId(userId);
                  localStorage.setItem(
                    "user",
                    JSON.stringify({
                      username: user.username,
                      userId: user.id
                    })
                  );
                } else {
                  const errData = await response.json();
                  alert(errData.detail || "Authentication failed");
                }
              } catch (err) {
                console.error("Auth error:", err);
              }
            }}
          >
            {isSignUp ? "Sign Up" : "Log In"}
          </button>
        </div>

        <p className='sign-up'
          onClick={() => setIsSignUp(!isSignUp)}

        >
          {isSignUp ? "Already have an account? Log in" : "Need an account? Sign up"}
        </p>
      </div>
    );
  }

  const incompleteCount = tasks.filter((task) => task.completed === 0).length;

  function handleInputChange(event) {
    setNewTask(event.target.value);
  }


  async function addItem() {
    if (newTask.trim() === "") return;

    const response = await fetch(`/todos?user_id=${userId}`, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        text: newTask,
        completed: 0,
      }),
    }
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Server Error (${response.status}):`, errorText);
      return;
    }


    const data = await response.json();



    setTasks(t => [...t, data]);
    setNewTask("");

  }

  async function completeTask(id) {

    const response = await fetch(
      `/todos?user_id=${userId}&todo_id=${id}`,
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
      `/todos?user_id=${userId}&todo_id=${id}`,
      {
        method: "DELETE",
      }
    );
    setTasks(tasks.filter(task => task.id !== id));
  }

  async function deleteUser(targetUserId) {
    const apiUrl = import.meta.env.VITE_API_URL || "";
    await fetch(`${apiUrl}/users?user_id=${targetUserId}`,
      {
        method: "DELETE",
      }
    );
  }

  function startEditing(id, text) {
    setEditingId(id);
    setEditText(text);
  }

  async function saveEdit(id) {
    if (editText.trim() === "") return;

    const todo = tasks.find(task => task.id === id);

    const response = await fetch(`/todos?user_id=${userId}&todo_id=${id}`, {
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
      return task.completed === 1;
    } else if (filter === "in progress") {
      return task.completed === 0;

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
          setPasswordInput("");
          setUserId(null);
          setTasks([]);
        }}
      >
        Log out
      </button>
      <button
        className="delete-user-button"
        onClick={() => {
          deleteUser(userId);
          localStorage.removeItem("user");
          setUsername("");
          setUsernameInput("");
          setPasswordInput("");
          setPassword("");
          setUserId(null);
          setTasks([]);

        }}
      >
        Delete User
      </button>
    </div >

  );
}
export default ToDo
