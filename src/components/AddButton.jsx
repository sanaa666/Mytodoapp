export default function AddButton({ addItem }) {
  return (
    <button
      className="add-button"
      onClick={addItem}>
      Add
    </button>
  );
}