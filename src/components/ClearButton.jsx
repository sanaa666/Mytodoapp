export default function ClearButton({ setTasks }) {
  return (
    <button onClick={() => setTasks(tasks => tasks.filter(task => !task.completed))} className="clear-button">Clear All Completed</button>
  );
}  