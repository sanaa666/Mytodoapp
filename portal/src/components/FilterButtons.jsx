export default function FilterButtons({ setFilter }) {
  return (    
    <div className="filter-buttons">
                <button onClick={() => setFilter("all")}>All</button>
                <button onClick={() => setFilter("completed")}>Completed</button>
                <button onClick={() => setFilter("in progress")}>Active</button>
    </div>
    );
}