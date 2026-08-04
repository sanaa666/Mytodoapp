export default function TasksContainer({ displayedTasks, editingId, editText, setEditText, startEditing, saveEdit, cancelEdit, completeTask, deleteTask }) {
  return (
    <div className="tasks-container">
            <ol>
                {displayedTasks.map((item)=>(
                  <li key={item.id}>
                    {editingId === item.id ? (
                      <div>
                        <input
                          type="text"
                          value={editText}
                          onChange={(e) => setEditText(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter") saveEdit(item.id);
                            if (e.key === "Escape") cancelEdit();
                          }}
                        />

                      <button className="save-button" onClick={() => saveEdit(item.id)}>Save</button>
                      <button className="cancel-button" onClick={cancelEdit}>Cancel</button>
                      </div>
                    ) : (
                      <div>
                        
                      
                        <span className={`text ${item.completed ?  "completed" : ""}`}
                        onDoubleClick={() => startEditing(item.id, item.text)}
                        style={{cursor: "pointer"}}>
                          {item.text}
                        </span>

                          <button
                            className="complete-button"
                            onClick= {() => completeTask(item.id)}>
                            {item.completed ? "Undo" : "Done"}
                          </button>
                          <button
                            className="delete-button"
                            onClick= {() => deleteTask(item.id)}>
                            Delete
                          </button>
                      </div>

                    )}
                    
                  </li>
              ))}
            </ol>
          </div>
    );
}
