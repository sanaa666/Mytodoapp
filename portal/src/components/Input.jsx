export default function Input({ newTask, handleInputChange, addItem }) {
  return (
    <input
                      type="text"
                      placeholder="Enter task..."
                      className="task-enter"
                      value={newTask}
                      onChange={handleInputChange}
                      onKeyDown={(e) => {
                            if (e.key === "Enter") {addItem};
                      }}/>
    );
}