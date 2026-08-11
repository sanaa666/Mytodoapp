export function Header({ incompleteCount }) {
    return (
        <div>
            {/* <h1>To Do</h1> */}
            <h3>Items still not complete: {incompleteCount}</h3>
        </div>
    )
}