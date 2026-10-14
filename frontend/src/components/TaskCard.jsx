const statuses = ["TODO", "IN_PROGRESS", "DONE"];

const labels = {
  TODO: "To Do",
  IN_PROGRESS: "In Progress",
  DONE: "Done",
};

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export default function TaskCard({ task, busy, onStatusChange, onDelete }) {
  return (
    <article className="task-card">
      <div className="task-copy">
        <div className="task-title-row">
          <h3>{task.title}</h3>
          <span className={`status-badge status-${task.status.toLowerCase()}`}>
            {labels[task.status]}
          </span>
        </div>
        <p className={task.description ? "description" : "description muted"}>
          {task.description || "No description provided."}
        </p>
        <p className="timestamp">Created {formatDate(task.created_at)}</p>
      </div>
      <div className="task-actions">
        <label className="sr-only" htmlFor={`status-${task.id}`}>
          Status for {task.title}
        </label>
        <select
          id={`status-${task.id}`}
          value={task.status}
          onChange={(event) => onStatusChange(task.id, event.target.value)}
          disabled={busy}
        >
          {statuses.map((status) => (
            <option key={status} value={status}>
              {labels[status]}
            </option>
          ))}
        </select>
        <button
          className="button button-danger button-small"
          onClick={() => onDelete(task.id)}
          disabled={busy}
        >
          Delete
        </button>
      </div>
    </article>
  );
}

