export default function AddButton({ addItem }) {
  return (
    <div>
    <button
      className="add-button"
      onClick={addItem}>
      Add
    </button>
    </div>
  );
}