import { useState } from "react";

export default function BoardSidebar({
  boards,
  selectedBoardId,
  loading,
  onSelect,
  onCreate,
}) {
  const [name, setName] = useState("");
  const [validation, setValidation] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim()) {
      setValidation("Board name is required.");
      return;
    }
    setValidation("");
    setSubmitting(true);
    try {
      await onCreate(name.trim());
      setName("");
    } catch (error) {
      setValidation(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <aside className="sidebar">
      <div>
        <p className="eyebrow">Workspace</p>
        <h1>Task Manager</h1>
        <p className="muted">Keep the team's work visible and organized.</p>
      </div>

      <form className="stack" onSubmit={handleSubmit} noValidate>
        <label htmlFor="board-name">New board</label>
        <div className="inline-form">
          <input
            id="board-name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="e.g. Q3 Website Refresh"
            maxLength={150}
            disabled={submitting}
          />
          <button className="button button-primary" disabled={submitting}>
            {submitting ? "Adding..." : "Add"}
          </button>
        </div>
        {validation && <p className="field-error">{validation}</p>}
      </form>

      <nav aria-label="Boards">
        <div className="section-heading">
          <h2>Boards</h2>
          <span className="count">{boards.length}</span>
        </div>
        {loading ? (
          <p className="muted">Loading boards...</p>
        ) : boards.length === 0 ? (
          <p className="empty-copy">No boards yet. Create the first board above.</p>
        ) : (
          <ul className="board-list">
            {boards.map((board) => (
              <li key={board.id}>
                <button
                  className={`board-button ${
                    board.id === selectedBoardId ? "active" : ""
                  }`}
                  onClick={() => onSelect(board.id)}
                >
                  <span>{board.name}</span>
                  <span aria-hidden="true">›</span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </nav>
    </aside>
  );
}

