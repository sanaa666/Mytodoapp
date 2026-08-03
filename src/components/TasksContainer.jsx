export default function TasksContainer({ displayedTasks, editingIndex, editText, setEditText, startEditing, saveEdit, cancelEdit, completeTask, deleteTask }) {
  return (
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
    );
}
